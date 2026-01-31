from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from jai.rag.models import Document, DocumentVersion
from jai.rag.enums import IngestionStatus, IngestionStage
from jai.rag.exceptions import DuplicateDocumentError


async def read_documents(session: AsyncSession):
    result = await session.execute(select(Document))
    return result.scalars().all()


async def read_document(session: AsyncSession, document_id: str):
    result = await session.execute(
        select(Document)
        .where(Document.document_id == document_id)
        .options(selectinload(Document.versions))
    )
    return result.scalar_one_or_none()


async def create_document(
    session: AsyncSession, file_name: str, file_hash: str
) -> tuple[Document, DocumentVersion]:
    document_result = await session.execute(
        select(Document).where(Document.file_name == file_name)
    )
    existing_document = document_result.scalar_one_or_none()

    # check if this filename already exists
    if existing_document:
        # check all versions of that file
        version_result = await session.execute(
            select(DocumentVersion.version, DocumentVersion.hash).where(
                DocumentVersion.document_pk == existing_document.id
            )
        )
        existing_versions = version_result.all()

        # if a version contains the same content return a Duplication Error
        if any(row.hash == file_hash for row in existing_versions):
            raise DuplicateDocumentError(
                f"Document '{file_name}' already contains this content in a previous version."
            )

        new_version_num = max((row.version for row in existing_versions), default=0) + 1

        existing_document.latest_version = new_version_num
        existing_document.latest_hash = file_hash
        existing_document.latest_status = IngestionStatus.PENDING
        existing_document.latest_stage = IngestionStage.RAW
        current_document = existing_document

    else:  # create a new document and version
        current_document = Document(
            file_name=file_name,
            latest_hash=file_hash,
            latest_status=IngestionStatus.PENDING,
            latest_stage=IngestionStage.RAW,
        )
        session.add(current_document)
        await session.flush()
        new_version_num = 1

    current_version = DocumentVersion(
        document_pk=current_document.id,
        version=new_version_num,
        hash=file_hash,
        status=IngestionStatus.PENDING,
        stage=IngestionStage.RAW,
    )
    session.add(current_version)
    await session.flush()
    await session.refresh(current_document)
    await session.refresh(current_version)

    return current_document, current_version

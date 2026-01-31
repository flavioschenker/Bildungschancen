from sqlalchemy import String, DateTime, Enum, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from jai.core import generate_id, PostgresBase
from jai.rag.enums import IngestionStatus, IngestionStage

from api.utils import PostgresBase

class Document(PostgresBase):
    __tablename__ = "documents"

    # id: Mapped[type] = mapped_column(...)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
        default=lambda: generate_id("document"),
    )

    file_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    latest_version: Mapped[int] = mapped_column(Integer, nullable=False)
    latest_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    latest_status: Mapped[IngestionStatus] = mapped_column(
        Enum(IngestionStatus, native_enum=True), nullable=False
    )
    latest_stage: Mapped[IngestionStage] = mapped_column(
        Enum(IngestionStatus, native_enum=True), nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    versions: Mapped[list["DocumentVersion"]] = relationship(
        "DocumentVersion",
        back_populates="document",
        order_by="desc(DocumentVersion.version)",
    )


class DocumentVersion(PostgresBase):
    __tablename__ = "documents_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    trace_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
        default=lambda: generate_id("trace"),
    )

    document_pk: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id")
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False)
    hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    status: Mapped[IngestionStatus] = mapped_column(
        Enum(IngestionStatus, native_enum=True), nullable=False
    )
    stage: Mapped[IngestionStage] = mapped_column(
        Enum(IngestionStatus, native_enum=True), nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    document: Mapped["Document"] = relationship("Document", back_populates="versions")

from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import skills
from api.schemas import SkillCreate, SkillRead, SkillDetail
from api.models import Skill

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.post("", response_model=SkillRead)
async def create_skill(
    skill_create: SkillCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Skill:
    async with postgres_client.get_session() as session:
        skill = await skills.create(session, skill_create)
        return skill
    

@router.get("", response_model=list[SkillRead])
async def get_skills(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Skill]:
    async with postgres_client.get_session() as session:
        return await skills.read_all(session)


@router.get("/{skill_id}", response_model=SkillDetail)
async def get_skill(
    skill_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Skill:
    async with postgres_client.get_session() as session:
        skill = await skills.read(session, skill_id)
        if skill is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Skill with id {skill_id} not found!")  
        return skill 
    

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        skill = await skills.delete(session, skill_id)
        if skill is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Skill with id {skill_id} not found!")
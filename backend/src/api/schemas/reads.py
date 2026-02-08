from pydantic import field_validator
from api.schemas.base import UserBase, SkillBase
from api.models import UserSkill

class UserRead(UserBase):
    user_id: str

class UserDetail(UserRead):
    skills: list[SkillRead]
    @field_validator("skills", mode="before")
    @classmethod
    def flatten_skills(cls, v:list[UserSkill]):
        return [i.skill for i in v]

class SkillRead(SkillBase):
    skill_id: str

class SkillDetail(SkillRead):
    users: list[UserRead]
    @field_validator("users", mode="before")
    @classmethod
    def flatten_users(cls, v:list[UserSkill]):
        return [i.user for i in v]
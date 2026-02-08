from api.schemas.base import UserBase, SkillBase

class UserCreate(UserBase):
    password: str
    skill_ids: list[str] | None = None

class SkillCreate(SkillBase):
    pass
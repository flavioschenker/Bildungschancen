from pydantic import BaseModel

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    skill_ids: list[str] | None = None


class SkillUpdate(BaseModel):
    name: str
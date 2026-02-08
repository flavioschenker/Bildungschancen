from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class SkillBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)
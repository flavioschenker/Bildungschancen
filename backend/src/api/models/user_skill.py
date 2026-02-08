from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase

if TYPE_CHECKING:
    from api.models.users import User
    from api.models.skills import Skill

class UserSkill(PostgresBase):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="skills")

    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship(back_populates="users")


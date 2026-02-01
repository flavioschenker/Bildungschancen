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

    user: Mapped["User"] = relationship(back_populates="skills")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    skill: Mapped["Skill"] = relationship(back_populates="users")
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"))

    description: Mapped[str | None] = mapped_column(Text)

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.user_skill import UserSkill

class Skill(PostgresBase):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("skill"))
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    users: Mapped[list["UserSkill"]] = relationship( back_populates="skill", passive_deletes="all")
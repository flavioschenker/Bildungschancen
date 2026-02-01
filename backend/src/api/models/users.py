from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.users import User
    from api.models.skills import Skill
    from api.models.user_skill import UserSkill

# This should not be exposed outside
class User(PostgresBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("user"))

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    password_hash: Mapped[str] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(100))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    skills: Mapped[list["UserSkill"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    sent_connections: Mapped[list["Connection"]] = relationship(back_populates="from_user")
    received_connections: Mapped[list["Connection"]] = relationship(back_populates="to_user")

class Connection(PostgresBase):
    __tablename__ = "connections"
    id: Mapped[int] = mapped_column(primary_key=True)

    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    from_user: Mapped["User"] = relationship(foreign_keys=[from_user_id], back_populates="sent_connections")

    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user: Mapped["User"] = relationship(foreign_keys=[to_user_id], back_populates="received_connections")
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, List

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.utils import PostgresBase

class User(PostgresBase):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship to Skills via the UserSkill association table
    skills: Mapped[list["UserSkill"]] = relationship(
        "UserSkill", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Relationships for the Social Graph (Connections)
    # 1. Requests sent by this user
    sent_connections: Mapped[List["Connection"]] = relationship(
        "Connection",
        foreign_keys="[Connection.from_user_id]",
        back_populates="from_user"
    )
    
    # 2. Requests received by this user
    received_connections: Mapped[List["Connection"]] = relationship(
        "Connection",
        foreign_keys="[Connection.to_user_id]",
        back_populates="to_user"
    )

    # Relationships for Messaging
    messages_sent: Mapped[List["Message"]] = relationship(
        "Message",
        foreign_keys="[Message.sender_id]",
        back_populates="sender"
    )
    messages_received: Mapped[List["Message"]] = relationship(
        "Message",
        foreign_keys="[Message.recipient_id]",
        back_populates="recipient"
    )

class Skill(PostgresBase):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Back-reference to see who has this skill
    user_associations: Mapped[List["UserSkill"]] = relationship(
        "UserSkill", 
        back_populates="skill"
    )

class UserSkill(PostgresBase):
    """
    Association table between User and Skill.
    Allows defining proficiency for a specific skill.
    """
    __tablename__ = "user_skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )

    proficiency: Mapped[ProficiencyLevel] = mapped_column(
        Enum(ProficiencyLevel, native_enum=True), 
        nullable=False, 
        default=ProficiencyLevel.BEGINNER
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_associations")

class Connection(PostgresBase):
    """
    Represents the edges in the social graph.
    """
    __tablename__ = "connections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    from_user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    to_user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    status: Mapped[ConnectionStatus] = mapped_column(
        Enum(ConnectionStatus, native_enum=True), 
        nullable=False, 
        default=ConnectionStatus.PENDING
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    from_user: Mapped["User"] = relationship(
        "User", foreign_keys=[from_user_id], back_populates="sent_connections"
    )
    to_user: Mapped["User"] = relationship(
        "User", foreign_keys=[to_user_id], back_populates="received_connections"
    )

class Message(PostgresBase):
    """
    Handles direct messages and introductions via intermediaries.
    """
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    
    # Optional: If this message is being routed via a friend (the link)
    intermediary_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_introduction: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    sender: Mapped["User"] = relationship(
        "User", foreign_keys=[sender_id], back_populates="messages_sent"
    )
    recipient: Mapped["User"] = relationship(
        "User", foreign_keys=[recipient_id], back_populates="messages_received"
    )
    intermediary: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[intermediary_id]
    )
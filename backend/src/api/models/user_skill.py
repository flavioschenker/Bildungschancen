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
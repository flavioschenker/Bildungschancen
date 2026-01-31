from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase

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
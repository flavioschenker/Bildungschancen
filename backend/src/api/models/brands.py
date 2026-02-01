from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient

class Brand(PostgresBase):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("brand"))
    name: Mapped[str]  = mapped_column(String(30))
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="brand")

    def __repr__(self) -> str:
            return f"<Brand(name='{self.name}', brand_id='{self.brand_id}')>"
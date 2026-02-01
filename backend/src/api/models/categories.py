from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient

class Category(PostgresBase):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("category"))
    name: Mapped[str]  = mapped_column(String(30))
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
            return f"<Category(name='{self.name}', category_id='{self.category_id}')>"
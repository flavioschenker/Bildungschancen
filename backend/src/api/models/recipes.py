from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.recipe_ingredients import RecipeIngredient

class Recipe(PostgresBase):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("recipe"))
    name: Mapped[str] = mapped_column(String(30))

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(back_populates="recipe")
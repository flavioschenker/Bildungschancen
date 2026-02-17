from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import UniqueConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient
    from api.models.recipes import Recipe
    from api.models.units import Unit


class RecipeIngredient(PostgresBase):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (UniqueConstraint("ingredient_id", "recipe_id", name="uq_recipe_ingredient"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    ingredient: Mapped["Ingredient"] = relationship(back_populates="in_recipes")
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"))

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))

    unit: Mapped["Unit"] = relationship()
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))
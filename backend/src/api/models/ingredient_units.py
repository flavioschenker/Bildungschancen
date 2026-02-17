from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient
    from api.models.units import Unit

class IngredientUnit(PostgresBase):
    __tablename__ = "ingredient_units"
    __table_args__ = (UniqueConstraint("ingredient_id", "unit_id", name="uq_ingredient_unit"),)
    id: Mapped[int] = mapped_column(primary_key=True)

    ingredient: Mapped["Ingredient"] = relationship(back_populates="supported_units")
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

    unit: Mapped["Unit"] = relationship()
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    relative_quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))
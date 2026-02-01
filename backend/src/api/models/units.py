from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient

class Unit(PostgresBase):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("unit"))
    name: Mapped[str] = mapped_column(String(30))
    symbol: Mapped[str] = mapped_column(String(3))
    base_unit_ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="base_unit")

    def __repr__(self) -> str:
            return f"<Unit(name='{self.name}', unit_id='{self.unit_id}')>"
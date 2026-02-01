from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.ingredients import Ingredient

class Currency(PostgresBase):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    currency_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("currency"))
    name: Mapped[str]  = mapped_column(String(30))
    symbol: Mapped[str] = mapped_column(String(3))
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="currency")
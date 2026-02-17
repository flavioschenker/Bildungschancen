from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.utils import PostgresBase, generate_id

if TYPE_CHECKING:
    from api.models.categories import Category
    from api.models.brands import Brand
    from api.models.units import Unit
    from api.models.sources import Source
    from api.models.currencies import Currency
    from api.models.ingredient_units import IngredientUnit
    from api.models.recipe_ingredients import RecipeIngredient

class Ingredient(PostgresBase):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[str] = mapped_column(String(30), unique=True, index=True, default=lambda: generate_id("ingredient"))
    name: Mapped[str]  = mapped_column(String(100), nullable=False)

    # Many-to-One relationships
    category: Mapped["Category"] = relationship(back_populates="ingredients")
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.category_id"))

    brand: Mapped["Brand"] = relationship(back_populates="ingredients")
    brand_id: Mapped[str] = mapped_column(ForeignKey("brands.brand_id"))

    base_unit: Mapped["Unit"] = relationship(back_populates="base_unit_ingredients")
    base_unit_id: Mapped[str] = mapped_column(ForeignKey("units.unit_id"))
    base_quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))

    package_quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    source: Mapped["Source"] = relationship(back_populates="ingredients")
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"))

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped["Currency"] = relationship(back_populates="ingredients")
    currency_id: Mapped[str] = mapped_column(ForeignKey("currencies.currency_id"))

    # Many-to-Many relationships
    supported_units: Mapped[list["IngredientUnit"]] = relationship(back_populates="ingredient", cascade="all, delete-orphan")
    in_recipes: Mapped[list["RecipeIngredient"]] = relationship(back_populates="ingredient", cascade="all, delete-orphan") # Do not delete whole recipe items

    # further attributes
    calories: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    protein: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    carbohydrates: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    carbohydrates_sugar: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    fat: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    fat_saturated: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    fiber: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    salt: Mapped[Decimal] = mapped_column(Numeric(10, 6))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
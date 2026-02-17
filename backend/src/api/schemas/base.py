from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class SkillBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class IngredientBase(BaseModel):
    name: str
    package_quantity: Decimal
    base_quantity: Decimal
    price: Decimal
    calories: Decimal
    protein: Decimal
    carbohydrates: Decimal
    carbohydrates_sugar: Decimal
    fat: Decimal
    fat_saturated: Decimal
    fiber: Decimal
    salt: Decimal

class UnitBase(BaseModel):
    name: str
    symbol: str
    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class BrandBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class SourceBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class CurrencyBase(BaseModel):
    name: str
    symbol: str
    model_config = ConfigDict(from_attributes=True)
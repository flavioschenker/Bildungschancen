from api.schemas.base import UserBase, SkillBase, IngredientBase, UnitBase, CategoryBase, BrandBase, SourceBase, CurrencyBase

class UserCreate(UserBase):
    password: str
    skill_ids: list[str] | None = None

class SkillCreate(SkillBase):
    pass

class IngredientCreate(IngredientBase):
    category_id: str
    brand_id: str
    base_unit_id: str
    source_id: str
    currency_id: str
    supported_units_ids: list[str] | None = None

class UnitCreate(UnitBase):
    pass

class CategoryCreate(CategoryBase):
    pass

class BrandCreate(BrandBase):
    pass

class SourceCreate(SourceBase):
    pass

class CurrencyCreate(CurrencyBase):
    pass
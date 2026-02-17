from pydantic import field_validator
from api.schemas.base import UserBase, SkillBase, IngredientBase, UnitBase, CategoryBase, BrandBase, SourceBase, CurrencyBase
from api.models import UserSkill, Category, Brand, Source, Currency

class UserRead(UserBase):
    user_id: str

class UserDetail(UserRead):
    skills: list[SkillRead]
    @field_validator("skills", mode="before")
    @classmethod
    def flatten_skills(cls, v:list[UserSkill]):
        return [i.skill for i in v]

class SkillRead(SkillBase):
    skill_id: str

class SkillDetail(SkillRead):
    users: list[UserRead]
    @field_validator("users", mode="before")
    @classmethod
    def flatten_users(cls, v:list[UserSkill]):
        return [i.user for i in v]
    

class IngredientRead(IngredientBase):
    base_unit: str
    @field_validator("base_unit", mode="before")
    @classmethod
    def flatten_base_unit(cls, c:Category):
        return c.name    
    category: str
    @field_validator("category", mode="before")
    @classmethod
    def flatten_category(cls, c:Category):
        return c.name
    brand: str
    @field_validator("brand", mode="before")
    @classmethod
    def flatten_brand(cls, b:Brand):
        return b.name    
    source: str
    @field_validator("source", mode="before")
    @classmethod
    def flatten_source(cls, s:Source):
        return s.name    
    currency: str
    @field_validator("currency", mode="before")
    @classmethod
    def flatten_currency(cls, c:Currency):
        return c.symbol    
    
class IngredientDetail(IngredientRead):
    pass

class UnitRead(UnitBase):
    unit_id: str

class UnitDetail(UnitRead):
    base_unit_ingredients: list[IngredientRead]

class CategoryRead(CategoryBase):
    category_id: str

class CategoryDetail(CategoryRead):
    ingredients: list[IngredientRead]

class BrandRead(BrandBase):
    brand_id: str

class BrandDetail(BrandRead):
    ingredients: list[IngredientRead]

class SourceRead(SourceBase):
    source_id: str

class SourceDetail(SourceRead):
    ingredients: list[IngredientRead]

class CurrencyRead(CurrencyBase):
    currency_id: str

class CurrencyDetail(CurrencyRead):
    ingredients: list[IngredientRead]

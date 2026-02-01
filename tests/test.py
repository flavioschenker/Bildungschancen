from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Brand(Base):
    __tablename__ = "brand"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Optional: Allow the Brand to see all its ingredients
    ingredients: Mapped[List["Ingredient"]] = relationship(back_populates="brand")

class Ingredient(Base):
    __tablename__ = "ingredient"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # The Foreign Key: Stores the ID of the brand
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    
    # The Relationship: Allows you to do 'my_ingredient.brand.name'
    brand: Mapped["Brand"] = relationship(back_populates="ingredients")


# WITHOUT back_populates
my_brand = Brand(name="OrganicCo")
my_ingred_2 = Ingredient(name="Flour", brand=my_brand)
my_ingred_1 = Ingredient(name="Fefelour", brand=my_brand)
my_brand.ingredients = []

print(my_ingred_2.brand)
print(my_brand.ingredients) 

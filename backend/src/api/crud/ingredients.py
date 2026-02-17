from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from api.models import Ingredient, Category, Brand, Unit, Source, Currency, IngredientUnit, RecipeIngredient
from api.schemas import IngredientCreate

async def create(session: AsyncSession, ingredient_create: IngredientCreate) -> Ingredient:
    ingredient_data = ingredient_create.model_dump(exclude={
        "supported_units_ids"
    })
    ingredient = Ingredient(
        **ingredient_data
    )
    if ingredient_create.supported_units_ids:
        result = await session.execute(
            select(Unit)
            .where(Unit.unit_id.in_(ingredient_create.supported_units_ids))
        )
        supported_units = result.scalars().all()
        for unit in supported_units:
            ingredient.supported_units.append(
                IngredientUnit(
                    unit=unit,
                    relative_quantity=0.0
                )
            )
    else:
        ingredient.supported_units = []
    session.add(ingredient)            
    await session.commit()

    created_ingredient = await read(session, ingredient.ingredient_id)
    if not created_ingredient:
        raise RuntimeError("Ingredient creation failed silently.")

    return created_ingredient


async def read_all(session: AsyncSession) -> Sequence[Ingredient]:
    result = await session.execute(
        select(Ingredient)
        .options(
            joinedload(Ingredient.category),
            joinedload(Ingredient.brand),
            joinedload(Ingredient.source),
            joinedload(Ingredient.base_unit),
            joinedload(Ingredient.currency)
        )
    )
    return result.scalars().unique().all()

async def read(session: AsyncSession, ingredient_id: str) -> Ingredient | None:
    result = await session.execute(
        select(Ingredient)
        .where(Ingredient.ingredient_id == ingredient_id)
        .options(
            joinedload(Ingredient.category),
            joinedload(Ingredient.brand),
            joinedload(Ingredient.source),
            joinedload(Ingredient.base_unit),
            joinedload(Ingredient.currency),
            selectinload(Ingredient.supported_units)
            .joinedload(IngredientUnit.unit),
            selectinload(Ingredient.in_recipes)
            .joinedload(RecipeIngredient.recipe)
        )
    )
    return result.scalar_one_or_none()
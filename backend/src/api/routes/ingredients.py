from fastapi import APIRouter, Depends
from collections.abc import Sequence
from api.crud import ingredients
from api.utils import PostgresClient
from api.schemas import IngredientCreate, IngredientRead, IngredientDetail
from api.models import Ingredient

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("", response_model=IngredientDetail)
async def create_ingredient(
    ingredient_create: IngredientCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Ingredient:
    async with postgres_client.get_session() as session:
        ingredient = await ingredients.create(session, ingredient_create)
        return ingredient

@router.get("", response_model=list[IngredientRead])
async def get_ingredients(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Ingredient]:
    async with postgres_client.get_session() as session:
        return await ingredients.read_all(session)
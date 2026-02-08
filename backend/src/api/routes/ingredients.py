from fastapi import APIRouter, Depends
from api.crud import read_ingredients, read_ingredient, create_ingredient, update_ingredient, delete_ingredient
from api.utils import PostgresClient
from api.schemas import IngredientRead, IngredientCreate, IngredientDetailRead

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.get("", response_model=list[IngredientRead])
async def get_users(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> list[IngredientRead]:
    async with postgres_client.get_session() as session:
        return await read_ingredients(session)
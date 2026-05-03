from pydantic import BaseModel
from app.schemas.ingredient import IngredientRead


class DishIngredientIn(BaseModel):
    ingredient_id: int
    weight_g: float


class DishIngredientRead(BaseModel):
    ingredient: IngredientRead
    weight_g: float

    model_config = {"from_attributes": True}


class DishCreate(BaseModel):
    name: str
    description: str | None = None
    servings: int = 1
    ingredients: list[DishIngredientIn]


class DishRead(BaseModel):
    id: int
    name: str
    description: str | None
    servings: int
    owner_id: int
    ingredients: list[DishIngredientRead]

    model_config = {"from_attributes": True}


class NutritionResult(BaseModel):
    calories: float
    proteins: float
    fats: float
    carbs: float
    total_cost: float
    total_weight_g: float
    per_serving: dict
    all_available: bool
    unavailable_ingredients: list[str]

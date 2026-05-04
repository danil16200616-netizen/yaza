from pydantic import BaseModel
from app.schemas.ingredient import IngredientRead
from app.schemas.cooking import CookingMethodRead, CookingMediumRead


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
    cooking_method_id: int | None = None
    cooking_medium_id: int | None = None
    medium_amount_g: float | None = None


class DishRead(BaseModel):
    id: int
    name: str
    description: str | None
    servings: int
    owner_id: int
    ingredients: list[DishIngredientRead]
    cooking_method: CookingMethodRead | None = None
    cooking_medium: CookingMediumRead | None = None
    medium_amount_g: float | None = None

    model_config = {"from_attributes": True}


class NutritionResult(BaseModel):
    # До обработки
    raw_calories: float
    raw_proteins: float
    raw_fats: float
    raw_carbs: float
    raw_weight_g: float
    # После обработки
    calories: float
    proteins: float
    fats: float
    carbs: float
    total_weight_g: float
    # Финансы и доступность
    total_cost: float
    per_serving: dict
    all_available: bool
    unavailable_ingredients: list[str]
    # Метод готовки
    cooking_method_name: str | None = None
    cooking_medium_name: str | None = None
    cooking_effect: str | None = None

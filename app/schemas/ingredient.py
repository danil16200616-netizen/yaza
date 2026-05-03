from pydantic import BaseModel


class IngredientCreate(BaseModel):
    name: str
    category: str = "Прочее"
    calories: float = 0.0
    proteins: float = 0.0
    fats: float = 0.0
    carbs: float = 0.0
    price_per_100g: float = 0.0
    is_available: bool = True
    unit: str = "г"


class IngredientRead(IngredientCreate):
    id: int

    model_config = {"from_attributes": True}


class IngredientUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbs: float | None = None
    price_per_100g: float | None = None
    is_available: bool | None = None
    unit: str | None = None

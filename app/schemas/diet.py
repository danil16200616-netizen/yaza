from pydantic import BaseModel
from datetime import date


class DietEntryCreate(BaseModel):
    meal_type: str           # breakfast | lunch | dinner | snack
    dish_id: int | None = None
    ingredient_id: int | None = None
    name: str
    weight_g: float = 100.0
    calories: float
    proteins: float
    fats: float
    carbs: float


class DietEntryRead(DietEntryCreate):
    id: int
    daily_diet_id: int

    model_config = {"from_attributes": True}


class DailyDietRead(BaseModel):
    id: int
    date: date
    target_calories: float
    entries: list[DietEntryRead]

    model_config = {"from_attributes": True}


class DailyDietUpdate(BaseModel):
    target_calories: float


class DaySummary(BaseModel):
    date: date
    total_calories: float
    total_proteins: float
    total_fats: float
    total_carbs: float
    target_calories: float
    pct: float              # % от нормы


class CalendarMonth(BaseModel):
    year: int
    month: int
    days: list[DaySummary]

from pydantic import BaseModel


class CookingMethodRead(BaseModel):
    id: int
    name: str
    icon: str
    description: str
    protein_factor: float
    fat_factor: float
    carb_factor: float
    weight_change_pct: float
    absorbs_medium: bool
    medium_absorption_pct: float

    model_config = {"from_attributes": True}


class CookingMediumRead(BaseModel):
    id: int
    name: str
    icon: str
    calories: float
    proteins: float
    fats: float
    carbs: float

    model_config = {"from_attributes": True}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dish import Dish, DishIngredient
from app.models.ingredient import Ingredient
from app.models.cooking import CookingMethod, CookingMedium
from app.models.user import User
from app.schemas.dish import DishCreate, DishRead, NutritionResult
from app.services.auth import get_current_user
from app.services.calculator import calculate_nutrition

router = APIRouter(prefix="/dishes", tags=["Блюда"])


@router.get("/", response_model=list[DishRead])
def list_my_dishes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Dish).filter(Dish.owner_id == user.id).all()


@router.get("/{dish_id}", response_model=DishRead)
def get_dish(dish_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dish = db.get(Dish, dish_id)
    if not dish or dish.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return dish


def _apply_cooking(dish: Dish, data: DishCreate) -> None:
    dish.cooking_method_id = data.cooking_method_id
    dish.cooking_medium_id = data.cooking_medium_id
    dish.medium_amount_g   = data.medium_amount_g


@router.post("/", response_model=DishRead, status_code=201)
def create_dish(data: DishCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dish = Dish(name=data.name, description=data.description, servings=data.servings, owner_id=user.id)
    _apply_cooking(dish, data)
    db.add(dish)
    db.flush()

    for item in data.ingredients:
        ing = db.get(Ingredient, item.ingredient_id)
        if not ing:
            raise HTTPException(status_code=400, detail=f"Ингредиент {item.ingredient_id} не найден")
        db.add(DishIngredient(dish_id=dish.id, ingredient_id=ing.id, weight_g=item.weight_g))

    db.commit()
    db.refresh(dish)
    return dish


@router.put("/{dish_id}", response_model=DishRead)
def update_dish(dish_id: int, data: DishCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dish = db.get(Dish, dish_id)
    if not dish or dish.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")

    dish.name        = data.name
    dish.description = data.description
    dish.servings    = data.servings
    _apply_cooking(dish, data)

    for di in list(dish.ingredients):
        db.delete(di)
    db.flush()

    for item in data.ingredients:
        ing = db.get(Ingredient, item.ingredient_id)
        if not ing:
            raise HTTPException(status_code=400, detail=f"Ингредиент {item.ingredient_id} не найден")
        db.add(DishIngredient(dish_id=dish.id, ingredient_id=ing.id, weight_g=item.weight_g))

    db.commit()
    db.refresh(dish)
    return dish


@router.delete("/{dish_id}", status_code=204)
def delete_dish(dish_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dish = db.get(Dish, dish_id)
    if not dish or dish.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    db.delete(dish)
    db.commit()


@router.get("/{dish_id}/nutrition", response_model=NutritionResult)
def get_nutrition(dish_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dish = db.get(Dish, dish_id)
    if not dish or dish.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return calculate_nutrition(dish)

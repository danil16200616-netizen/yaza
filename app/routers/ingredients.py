from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ingredient import Ingredient
from app.models.user import User
from app.schemas.ingredient import IngredientCreate, IngredientRead, IngredientUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/ingredients", tags=["Ингредиенты"])


@router.get("/", response_model=list[IngredientRead])
def list_ingredients(
    search: str | None = Query(None),
    category: str | None = Query(None),
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    q = db.query(Ingredient)
    if search:
        q = q.filter(Ingredient.name.ilike(f"%{search}%"))
    if category:
        q = q.filter(Ingredient.category == category)
    if available_only:
        q = q.filter(Ingredient.is_available == True)
    return q.order_by(Ingredient.name).all()


@router.get("/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ing = db.get(Ingredient, ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    return ing


@router.post("/", response_model=IngredientRead, status_code=201)
def create_ingredient(
    data: IngredientCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if db.query(Ingredient).filter(Ingredient.name == data.name).first():
        raise HTTPException(status_code=400, detail="Ингредиент с таким именем уже существует")
    ing = Ingredient(**data.model_dump())
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing


@router.patch("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ing = db.get(Ingredient, ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ing, field, value)
    db.commit()
    db.refresh(ing)
    return ing


@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ing = db.get(Ingredient, ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    db.delete(ing)
    db.commit()

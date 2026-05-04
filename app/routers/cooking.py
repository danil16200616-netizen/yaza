from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cooking import CookingMethod, CookingMedium
from app.schemas.cooking import CookingMethodRead, CookingMediumRead

router = APIRouter(prefix="/cooking", tags=["Готовка"])


@router.get("/methods", response_model=list[CookingMethodRead])
def list_methods(db: Session = Depends(get_db)):
    return db.query(CookingMethod).order_by(CookingMethod.id).all()


@router.get("/mediums", response_model=list[CookingMediumRead])
def list_mediums(db: Session = Depends(get_db)):
    return db.query(CookingMedium).order_by(CookingMedium.id).all()

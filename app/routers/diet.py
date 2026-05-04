from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import date
from app.database import get_db
from app.models.diet import DailyDiet, DietEntry
from app.models.user import User
from app.schemas.diet import (
    DietEntryCreate, DietEntryRead,
    DailyDietRead, DailyDietUpdate,
    DaySummary, CalendarMonth,
)
from app.services.auth import get_current_user

router = APIRouter(prefix="/diet", tags=["Дневник питания"])


def _get_or_create_day(db: Session, user_id: int, day: date) -> DailyDiet:
    record = db.query(DailyDiet).filter(
        DailyDiet.user_id == user_id,
        DailyDiet.date == day,
    ).first()
    if not record:
        record = DailyDiet(user_id=user_id, date=day)
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


# ВАЖНО: специфичные маршруты — ВЫШЕ параметрических /{day}
@router.get("/today", response_model=DailyDietRead)
def get_today(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return _get_or_create_day(db, user.id, date.today())


@router.get("/calendar/{year}/{month}", response_model=CalendarMonth)
def get_calendar(year: int, month: int,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    records = db.query(DailyDiet).filter(
        DailyDiet.user_id == user.id,
        extract("year",  DailyDiet.date) == year,
        extract("month", DailyDiet.date) == month,
    ).all()

    days = []
    for rec in records:
        total_cal  = sum(e.calories for e in rec.entries)
        total_prot = sum(e.proteins for e in rec.entries)
        total_fat  = sum(e.fats     for e in rec.entries)
        total_carb = sum(e.carbs    for e in rec.entries)
        pct = round(total_cal / rec.target_calories * 100, 1) if rec.target_calories else 0
        days.append(DaySummary(
            date=rec.date,
            total_calories=round(total_cal,  1),
            total_proteins=round(total_prot, 1),
            total_fats=round(total_fat,      1),
            total_carbs=round(total_carb,    1),
            target_calories=rec.target_calories,
            pct=pct,
        ))

    days.sort(key=lambda d: d.date)
    return CalendarMonth(year=year, month=month, days=days)


@router.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.get(DietEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if entry.daily_diet.user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    db.delete(entry)
    db.commit()


# Параметрические маршруты — ПОСЛЕ специфичных
@router.get("/{day}", response_model=DailyDietRead)
def get_day(day: date, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return _get_or_create_day(db, user.id, day)


@router.patch("/{day}/target", response_model=DailyDietRead)
def update_target(day: date, data: DailyDietUpdate,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    record = _get_or_create_day(db, user.id, day)
    record.target_calories = data.target_calories
    db.commit()
    db.refresh(record)
    return record


@router.post("/{day}/entries", response_model=DietEntryRead, status_code=201)
def add_entry(day: date, data: DietEntryCreate,
              db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    record = _get_or_create_day(db, user.id, day)
    entry = DietEntry(
        daily_diet_id=record.id,
        meal_type=data.meal_type,
        dish_id=data.dish_id,
        ingredient_id=data.ingredient_id,
        name=data.name,
        weight_g=data.weight_g,
        calories=data.calories,
        proteins=data.proteins,
        fats=data.fats,
        carbs=data.carbs,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

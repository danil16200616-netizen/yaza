from sqlalchemy import String, Float, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime


class DailyDiet(Base):
    __tablename__ = "daily_diets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    target_calories: Mapped[float] = mapped_column(Float, default=2000.0)

    user: Mapped["User"] = relationship("User")
    entries: Mapped[list["DietEntry"]] = relationship(
        "DietEntry", back_populates="daily_diet", cascade="all, delete-orphan"
    )


class DietEntry(Base):
    __tablename__ = "diet_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_diet_id: Mapped[int] = mapped_column(ForeignKey("daily_diets.id"))
    # breakfast | lunch | dinner | snack
    meal_type: Mapped[str] = mapped_column(String(20))

    # Источник: блюдо из коллекции или ингредиент или ручной ввод
    dish_id: Mapped[int | None] = mapped_column(ForeignKey("dishes.id"), nullable=True)
    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredients.id"), nullable=True)

    name: Mapped[str] = mapped_column(String(200))
    weight_g: Mapped[float] = mapped_column(Float, default=100.0)

    # Итоговые нутриенты (уже пересчитанные на вес порции)
    calories: Mapped[float] = mapped_column(Float, default=0.0)
    proteins: Mapped[float] = mapped_column(Float, default=0.0)
    fats: Mapped[float] = mapped_column(Float, default=0.0)
    carbs: Mapped[float] = mapped_column(Float, default=0.0)

    daily_diet: Mapped["DailyDiet"] = relationship("DailyDiet", back_populates="entries")
    dish: Mapped["Dish | None"] = relationship("Dish")
    ingredient: Mapped["Ingredient | None"] = relationship("Ingredient")

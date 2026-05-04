from sqlalchemy import String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class CookingMethod(Base):
    __tablename__ = "cooking_methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    icon: Mapped[str] = mapped_column(String(10), default="🍳")
    description: Mapped[str] = mapped_column(Text, default="")

    # Коэффициенты сохранности нутриентов (1.0 = без потерь)
    protein_factor: Mapped[float] = mapped_column(Float, default=1.0)
    fat_factor: Mapped[float] = mapped_column(Float, default=1.0)
    carb_factor: Mapped[float] = mapped_column(Float, default=1.0)

    # Изменение веса блюда в % (отрицательное = потеря влаги)
    weight_change_pct: Mapped[float] = mapped_column(Float, default=0.0)

    # Поглощает ли блюдо среду готовки (масло и т.д.)
    absorbs_medium: Mapped[bool] = mapped_column(Boolean, default=False)
    # Какой % от добавленной среды поглощается продуктом
    medium_absorption_pct: Mapped[float] = mapped_column(Float, default=0.0)


class CookingMedium(Base):
    __tablename__ = "cooking_mediums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    icon: Mapped[str] = mapped_column(String(10), default="💧")

    # Нутриенты на 100г/100мл
    calories: Mapped[float] = mapped_column(Float, default=0.0)
    proteins: Mapped[float] = mapped_column(Float, default=0.0)
    fats: Mapped[float] = mapped_column(Float, default=0.0)
    carbs: Mapped[float] = mapped_column(Float, default=0.0)

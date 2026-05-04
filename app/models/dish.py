from sqlalchemy import String, Float, ForeignKey, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    servings: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="dishes")

    # Метод и среда приготовления
    cooking_method_id: Mapped[int | None] = mapped_column(ForeignKey("cooking_methods.id"), nullable=True)
    cooking_medium_id: Mapped[int | None] = mapped_column(ForeignKey("cooking_mediums.id"), nullable=True)
    medium_amount_g: Mapped[float | None] = mapped_column(Float, nullable=True)

    cooking_method: Mapped["CookingMethod | None"] = relationship("CookingMethod")
    cooking_medium: Mapped["CookingMedium | None"] = relationship("CookingMedium")

    ingredients: Mapped[list["DishIngredient"]] = relationship(
        "DishIngredient", back_populates="dish", cascade="all, delete-orphan"
    )


class DishIngredient(Base):
    __tablename__ = "dish_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    weight_g: Mapped[float] = mapped_column(Float)

    dish: Mapped["Dish"] = relationship("Dish", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="dish_ingredients")

from app.models.dish import Dish


def calculate_nutrition(dish: Dish) -> dict:
    # ── 1. Базовый расчёт по ингредиентам ──────────────────────────
    raw = {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0,
           "total_cost": 0.0, "total_weight_g": 0.0}
    unavailable = []

    for di in dish.ingredients:
        ing = di.ingredient
        factor = di.weight_g / 100
        raw["calories"]     += ing.calories      * factor
        raw["proteins"]     += ing.proteins      * factor
        raw["fats"]         += ing.fats          * factor
        raw["carbs"]        += ing.carbs         * factor
        raw["total_cost"]   += ing.price_per_100g * factor
        raw["total_weight_g"] += di.weight_g
        if not ing.is_available:
            unavailable.append(ing.name)

    # ── 2. Применяем метод термической обработки ───────────────────
    method = dish.cooking_method
    medium = dish.cooking_medium
    medium_g = dish.medium_amount_g or 0.0

    cooked_proteins = raw["proteins"]
    cooked_fats     = raw["fats"]
    cooked_carbs    = raw["carbs"]
    cooked_weight   = raw["total_weight_g"]
    cooking_effect  = None
    method_name     = None
    medium_name     = None

    if method:
        method_name = method.name
        cooked_proteins *= method.protein_factor
        cooked_fats     *= method.fat_factor
        cooked_carbs    *= method.carb_factor
        cooked_weight   *= (1 + method.weight_change_pct / 100)

        # Поглощение среды приготовления (масло при жарке и т.д.)
        if method.absorbs_medium and medium and medium_g > 0:
            medium_name = medium.name
            absorbed_g = medium_g * (method.medium_absorption_pct / 100)
            cooked_proteins += medium.proteins * absorbed_g / 100
            cooked_fats     += medium.fats     * absorbed_g / 100
            cooked_carbs    += medium.carbs    * absorbed_g / 100
            cooked_weight   += absorbed_g

        # Описание эффекта
        delta_cal = round(
            (cooked_proteins * 4 + cooked_fats * 9 + cooked_carbs * 4) -
            (raw["proteins"]  * 4 + raw["fats"]  * 9 + raw["carbs"]  * 4)
        )
        weight_delta = round(cooked_weight - raw["total_weight_g"], 1)
        sign_cal = "+" if delta_cal >= 0 else ""
        sign_w   = "+" if weight_delta >= 0 else ""
        cooking_effect = (
            f"{method.name}"
            + (f" в {medium.name.lower()}" if medium and not method.absorbs_medium else "")
            + (f" с {medium.name.lower()} ({medium_g}г)" if medium and method.absorbs_medium else "")
            + f" → {sign_cal}{delta_cal} ккал, {sign_w}{weight_delta}г"
        )
    elif medium and medium_g > 0:
        medium_name = medium.name

    cooked_calories = round(cooked_proteins * 4 + cooked_fats * 9 + cooked_carbs * 4, 1)

    # ── 3. Итоговый результат ───────────────────────────────────────
    servings = dish.servings or 1
    per_serving = {
        "calories": round(cooked_calories / servings, 1),
        "proteins": round(cooked_proteins  / servings, 1),
        "fats":     round(cooked_fats      / servings, 1),
        "carbs":    round(cooked_carbs     / servings, 1),
        "cost":     round(raw["total_cost"] / servings, 2),
    }

    return {
        # До обработки
        "raw_calories": round(raw["proteins"] * 4 + raw["fats"] * 9 + raw["carbs"] * 4, 1),
        "raw_proteins": round(raw["proteins"], 1),
        "raw_fats":     round(raw["fats"],     1),
        "raw_carbs":    round(raw["carbs"],    1),
        "raw_weight_g": round(raw["total_weight_g"], 1),
        # После обработки
        "calories":     cooked_calories,
        "proteins":     round(cooked_proteins, 1),
        "fats":         round(cooked_fats,     1),
        "carbs":        round(cooked_carbs,    1),
        "total_weight_g": round(cooked_weight, 1),
        # Финансы
        "total_cost":   round(raw["total_cost"], 2),
        "per_serving":  per_serving,
        # Доступность
        "all_available":          len(unavailable) == 0,
        "unavailable_ingredients": unavailable,
        # Метаданные готовки
        "cooking_method_name": method_name,
        "cooking_medium_name": medium_name,
        "cooking_effect":      cooking_effect,
    }

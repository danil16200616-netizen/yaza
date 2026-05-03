from app.models.dish import Dish


def calculate_nutrition(dish: Dish) -> dict:
    totals = {
        "calories": 0.0,
        "proteins": 0.0,
        "fats": 0.0,
        "carbs": 0.0,
        "total_cost": 0.0,
        "total_weight_g": 0.0,
    }
    unavailable = []

    for di in dish.ingredients:
        ing = di.ingredient
        factor = di.weight_g / 100

        totals["calories"] += ing.calories * factor
        totals["proteins"] += ing.proteins * factor
        totals["fats"] += ing.fats * factor
        totals["carbs"] += ing.carbs * factor
        totals["total_cost"] += ing.price_per_100g * factor
        totals["total_weight_g"] += di.weight_g

        if not ing.is_available:
            unavailable.append(ing.name)

    servings = dish.servings or 1
    totals["per_serving"] = {
        "calories": round(totals["calories"] / servings, 1),
        "proteins": round(totals["proteins"] / servings, 1),
        "fats": round(totals["fats"] / servings, 1),
        "carbs": round(totals["carbs"] / servings, 1),
        "cost": round(totals["total_cost"] / servings, 2),
    }
    totals["calories"] = round(totals["calories"], 1)
    totals["proteins"] = round(totals["proteins"], 1)
    totals["fats"] = round(totals["fats"], 1)
    totals["carbs"] = round(totals["carbs"], 1)
    totals["total_cost"] = round(totals["total_cost"], 2)
    totals["all_available"] = len(unavailable) == 0
    totals["unavailable_ingredients"] = unavailable

    return totals

"""Наполнение базы методами и средами приготовления."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.cooking import CookingMethod, CookingMedium

METHODS = [
    # name, icon, desc, protein_f, fat_f, carb_f, weight_chg%, absorbs, absorption%
    ("Без обработки (сырой)", "🥗", "Продукт используется в исходном виде",
     1.0,  1.0,  1.0,   0.0,  False, 0.0),
    ("Варка в воде",          "🫕", "Потеря водорастворимых нутриентов в бульон",
     0.92, 0.95, 0.96, -15.0, False, 0.0),
    ("Варка в бульоне",       "🍲", "Часть нутриентов переходит в бульон, часть поглощается",
     0.93, 0.96, 0.97, -12.0, False, 0.0),
    ("Варка на пару",         "♨️",  "Лучшее сохранение нутриентов, минимальные потери",
     0.97, 0.98, 0.98,  -5.0, False, 0.0),
    ("Жарка с маслом",        "🍳", "Потеря влаги, поглощение масла из среды готовки",
     0.95, 1.0,  0.95, -25.0, True,  12.0),
    ("Жарка без масла (сухая)","🥘", "Только потеря влаги, без поглощения жира",
     0.95, 0.93, 0.95, -25.0, False, 0.0),
    ("Жарка во фритюре",      "🍟", "Значительное поглощение масла, большая потеря влаги",
     0.94, 1.0,  0.92, -30.0, True,  20.0),
    ("Запекание в духовке",   "🔥", "Умеренная потеря влаги, хорошее сохранение нутриентов",
     0.95, 0.97, 0.96, -20.0, False, 0.0),
    ("Тушение",               "🫙", "Медленное приготовление, хорошее сохранение нутриентов",
     0.94, 0.97, 0.97, -10.0, False, 0.0),
    ("Гриль / Мангал",        "🍖", "Жир вытапливается и стекает, высокая потеря влаги",
     0.95, 0.75, 0.96, -30.0, False, 0.0),
    ("Копчение",              "🫧", "Потеря влаги, минимальные изменения нутриентов",
     0.96, 0.97, 0.97, -35.0, False, 0.0),
    ("Варка + обжарка",       "🥗", "Двухэтапная обработка: варка затем обжарка с маслом",
     0.90, 1.0,  0.93, -30.0, True,  8.0),
]

MEDIUMS = [
    # name, icon, cal, proteins, fats, carbs
    ("Вода",                   "💧", 0.0,   0.0,  0.0,  0.0),
    ("Куриный бульон",         "🍗", 15.0,  1.5,  0.5,  0.5),
    ("Говяжий бульон",         "🥩", 20.0,  2.0,  0.8,  0.3),
    ("Овощной бульон",         "🥦", 10.0,  0.5,  0.2,  1.5),
    ("Растительное масло",     "🫙", 899.0, 0.0,  99.9, 0.0),
    ("Оливковое масло",        "🫒", 884.0, 0.0,  100.0,0.0),
    ("Сливочное масло",        "🧈", 748.0, 0.8,  82.5, 0.8),
    ("Животный жир (смалец)",  "🥓", 898.0, 0.0,  99.6, 0.0),
    ("Кокосовое масло",        "🥥", 892.0, 0.0,  99.1, 0.0),
    ("Топлёное масло",         "✨", 892.0, 0.3,  99.0, 0.0),
]


def seed():
    db = SessionLocal()
    try:
        existing_m = {m.name for m in db.query(CookingMethod.name).all()}
        existing_e = {m.name for m in db.query(CookingMedium.name).all()}

        new_methods = []
        for row in METHODS:
            name, icon, desc, pf, ff, cf, wc, absorb, abspct = row
            if name not in existing_m:
                new_methods.append(CookingMethod(
                    name=name, icon=icon, description=desc,
                    protein_factor=pf, fat_factor=ff, carb_factor=cf,
                    weight_change_pct=wc, absorbs_medium=absorb,
                    medium_absorption_pct=abspct,
                ))

        new_mediums = []
        for row in MEDIUMS:
            name, icon, cal, pro, fat, carb = row
            if name not in existing_e:
                new_mediums.append(CookingMedium(
                    name=name, icon=icon,
                    calories=cal, proteins=pro, fats=fat, carbs=carb,
                ))

        if new_methods:
            db.add_all(new_methods)
        if new_mediums:
            db.add_all(new_mediums)
        db.commit()
        print(f"Добавлено методов: {len(new_methods)}, сред: {len(new_mediums)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

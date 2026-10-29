"""Скачивает рецепты из TheMealDB и сохраняет их в data/recipes.csv."""

import csv
import json
import string
import time
import urllib.request
from pathlib import Path

API = "https://www.themealdb.com/api/json/v1/1/search.php?f="
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_meals(letter):
    """Возвращает список рецептов, название которых начинается на letter."""
    with urllib.request.urlopen(API + letter, timeout=30) as response:
        return json.load(response)["meals"] or []


def get_ingredients(meal):
    """Собирает ингредиенты рецепта в строки вида "500g raw king prawns"."""
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip().lower()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if name:
            ingredients.append(f"{measure} {name}".strip())
    return ingredients


meals = {}
for letter in string.ascii_lowercase:
    for meal in get_meals(letter):
        meals[meal["idMeal"]] = meal
    time.sleep(0.3)

DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "recipes.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "category", "ingredients", "instructions"])
    for meal in sorted(meals.values(), key=lambda meal: int(meal["idMeal"])):
        writer.writerow([
            meal["idMeal"],
            meal["strMeal"],
            meal["strCategory"] or "",
            "; ".join(get_ingredients(meal)),
            meal["strInstructions"] or "",
        ])

print(f"Сохранено рецептов: {len(meals)}")

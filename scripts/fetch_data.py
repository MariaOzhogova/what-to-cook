# Скачиваю рецепты из TheMealDB и сохраняю в data/recipes.csv
# Запускать из папки проекта: python scripts/fetch_data.py

import csv
import time
import requests

url = "https://www.themealdb.com/api/json/v1/1/search.php"

# API умеет искать рецепты по первой букве названия,
# поэтому прохожу по всем буквам алфавита
recipes = []
for letter in "abcdefghijklmnopqrstuvwxyz":
    response = requests.get(url, params={"f": letter}, timeout=10)
    response.raise_for_status()
    meals = response.json()["meals"]
    if meals is None:  # на некоторые буквы рецептов нет
        continue
    for meal in meals:
        recipes.append(meal)
    time.sleep(0.5)  # чтобы не заваливать сервер запросами

with open("data/recipes.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "category", "ingredients", "instructions"])
    for meal in recipes:
        # ингредиенты лежат в полях strIngredient1 ... strIngredient20
        ingredients = []
        for i in range(1, 21):
            name = meal["strIngredient" + str(i)]
            if name is None or name.strip() == "":
                continue
            name = name.strip().lower()
            if name not in ingredients:  # бывает, что продукт указан дважды
                ingredients.append(name)
        writer.writerow([meal["idMeal"], meal["strMeal"], meal["strCategory"],
                         ";".join(ingredients), meal["strInstructions"]])

print("Сохранено рецептов:", len(recipes))

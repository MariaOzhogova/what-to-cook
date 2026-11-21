# Анализ данных для проекта 

#анализирую, чтобы узнать следующее:
# 1. Сколько продуктов нужно для одного рецепта

#библиотеки и загрузка рецептов
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("data/recipes.csv")
print("Всего рецептов:", len(df))
print()


# 1. Сколько продуктов нужно для одного рецепта
counts = []
for text in df["ingredients"]:
    counts.append(len(text.split(";"))) #разделены через ;
counts = np.array(counts)
print("В среднем продуктов в рецепте:", round(np.mean(counts), 1))
print("Меньше всего:", np.min(counts))
print("Больше всего:", np.max(counts))
print()
plt.hist(counts, bins=20)
plt.title("Сколько продуктов нужно для одного блюда")
plt.xlabel("Сколько продуктов")
plt.ylabel("Сколько рецептов")
plt.savefig("analysis/1_picture.png")
plt.show()

# 2. Какие продукты нужны чаще всего
# собираем все продукты из всех рецептов в один список
all_products = []
for text in df["ingredients"]:
    for product in text.split(";"):
        all_products.append(product)
popular = pd.Series(all_products).value_counts() # value_counts считает, сколько раз встречается каждый продукт
print("Самые частые продукты:")
print(popular.head(10))
print()
top = popular.head(10)
plt.bar(top.index, top.values)
plt.xticks(rotation=45)
plt.title("10 самых частых продуктов")
plt.ylabel("В скольких рецептах")
plt.tight_layout()
plt.savefig("analysis/2_picture.png")
plt.show()


# 3. Сколько рецептов в каждой категории
categories = df["category"].value_counts()
print("Рецептов по категориям:")
print(categories)
print()
plt.bar(categories.index, categories.values)
plt.xticks(rotation=45)
plt.title("Рецепты по категориям")
plt.ylabel("Сколько рецептов")
plt.tight_layout()
plt.savefig("analysis/3_picture.png")
plt.show()


# 4. Что можно приготовить из того, что есть дома
my_products = ["salt", "pepper", "sugar", "water",
               "onion", "garlic", "potatoes", "carrots", "tomatoes",
               "eggs", "milk", "butter", "flour", "plain flour",
               "oil", "rice", "chicken", "chicken"] # продукты, которые обычно есть у меня
# для каждого рецепта считаем, скольких продуктов у меня нет
missing = []
for text in df["ingredients"]:
    n = 0
    for product in text.split(";"):
        if product not in my_products:
            n = n + 1
    missing.append(n)
missing = np.array(missing)
print("Можно приготовить сразу:", np.sum(missing == 0))
print("Не хватает 1 продукта:", np.sum(missing == 1))
print("Не хватает 2 продуктов:", np.sum(missing == 2))
# сколько рецептов, где не хватает х продуктов
numbers = []
for i in range(11):
    numbers.append(np.sum(missing == i))
plt.bar(range(11), numbers)
plt.xticks(range(11))
plt.title("Чего не хватает до рецепта с моими продуктами")
plt.xlabel("Скольких продуктов не хватает")
plt.ylabel("Сколько рецептов")
plt.savefig("analysis/4_picture.png")
plt.show()

# Вывод: сразу можно приготовить очень мало рецептов,
# а если докупить 1-2 продукта - намного больше.

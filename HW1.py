import requests
import json
API_KEY = 'b7a1c4be82554728bdecf8dff335fb1c'

# Идентификатор рецепта
RECIPE_ID = '645354'

# Адрес конечной точки API
url = f'https://api.spoonacular.com/recipes/{RECIPE_ID}/information?includeNutrition=true&apiKey={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Выводим основную информацию о пищевой ценности
    print("Название:", data["title"])
    print("Вид:", data["image"])
    print("Состав:", data["nutrition"]["nutrients"])
    print("\n")
else:
    print("Ошибка:", response.text)
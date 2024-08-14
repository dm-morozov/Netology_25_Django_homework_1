from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'pizza': {
        'тесто, г': 300,
        'томатный соус, г': 100,
        'сыр моцарелла, г': 150,
        'ветчина, г': 100,
        'грибы, г': 80,
        'оливковое масло, ст.л.': 1,
    },
    'caesar_salad': {
        'листья салата, г': 200,
        'куриная грудка, г': 150,
        'сухарики, г': 50,
        'пармезан, г': 30,
        'соус цезарь, ст.л.': 2,
    },
    'borsch': {
        'свекла, шт': 2,
        'картофель, шт': 3,
        'капуста, г': 200,
        'морковь, шт': 1,
        'лук, шт': 1,
        'томатная паста, ст.л.': 2,
        'говядина, г': 300,
        'вода, л': 1.5,
    },
    'pancakes': {
        'мука, г': 200,
        'молоко, мл': 300,
        'яйца, шт': 2,
        'сахар, ст.л.': 2,
        'соль, щепотка': 1,
        'растительное масло, ст.л.': 2,
    }
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def recipe(request, recipe):
    
    recipe = recipe.lower()

    try:
        servings = int(request.GET.get('servings', 1))
    except ValueError:
        servings = 1

    if recipe in DATA:
        content = {
            'name': recipe,
            'servings': servings,
            'recipe': {key: value * int(servings) for key, value in DATA[recipe].items()}

        }
    else:
        content = {
            'recipe': {},
            'name_recipe': ', '.join([key for key in DATA.keys()])
        }

    return render(request, 'calculator/index.html', content)
# Обработка запросов и шаблоны

Необходимо выполнить и предоставить на проверку следующие задачи:

1. [Рецепты](./recipes).

## Дополнительные задания:

1. [Пагинация](./pagination).

Присылать на проверку нужно сразу все обязательные задачи. Дополнительные задачи не влияют на получение зачёта.

Работы должны соответствовать
принятому [стилю оформления кода](https://github.com/netology-code/codestyle/tree/master/python).

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Что было сделано

### Проект 1: **Рецепты**

Этот проект представляет собой сервис-помощник для приготовления блюд. Сервис отображает рецепты на основе запроса пользователя. Каждый рецепт содержит список ингредиентов и их количество на одну порцию. Пользователь может изменить количество порций, передав соответствующий параметр.

**Функционал:**

- Список рецептов доступен через URL. Например, `/omlet/` для рецепта омлета.
- В случае добавления параметра `servings` (например, `/omlet/?servings=4`), ингредиенты пересчитываются для указанного числа порций.

**Примеры рецептов:**

```python
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
    ...
}
```

**Ключевые файлы:**

- `views.py`: Обрабатывает запросы и генерирует контекст для шаблона.
- `urls.py`: Маршрутизация запросов к рецептам.
- `index.html`: Шаблон для отображения ингредиентов.

**Запуск проекта:**

1. Установите зависимости:
    
    ```bash
    pip install -r requirements.txt
    ```
    
2. Запустите сервер:
    
    ```bash
    python manage.py runserver
    ```
    
3. Перейдите по адресу, например: `http://127.0.0.1:8000/omlet/`.

---

### Проект 2: **Пагинация**

Этот проект реализует пагинацию для отображения большого количества данных на нескольких страницах. В качестве примера используется список автобусных станций, который отображается постранично с возможностью навигации.

**Функционал:**

- Чтение данных из CSV-файла с автобусными станциями.
- Пагинация списка станций: каждая страница отображает 10 станций с возможностью перехода на следующую страницу.

**Ключевые файлы:**

- `views.py`: Обрабатывает запросы и передает данные для отображения постранично.
- `urls.py`: Маршрутизация запросов для станций.
- `index.html`: Шаблон для отображения станций с пагинацией.

**Пример кода:**

```python
def bus_stations(request):
    with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        bus_stations_list = list(reader)

    paginator = Paginator(bus_stations_list, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
```

**Запуск проекта:**

1. Установите зависимости:
    
    ```bash
    pip install -r requirements.txt
    ```
    
2. Запустите сервер:
    
    ```bash
    python manage.py runserver
    ```
    
3. Перейдите по адресу, например: `http://127.0.0.1:8000/bus_stations/?page=1`.

---

### Итоги

Два проекта были разработаны для учебной задачи на тему обработки запросов и шаблонов в Django. Проекты демонстрируют реализацию базовых возможностей Django: динамическое создание страниц на основе данных (рецепты и пагинация), использование шаблонов для визуализации данных и маршрутизацию запросов.
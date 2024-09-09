# Склады и товары

## Техническая задача

Реализовать CRUD-логику для продуктов и складов, используя Django Rest Framework (DRF). CRUD — это аббревиатура для Create-Read-Update-Delete, обозначающая базовые операции с сущностями.

## Описание

В рамках проекта реализовано REST API для управления продуктами и складами. Продукты имеют название и описание, а склады хранят информацию о наличии продуктов, их количестве и цене. Для хранения информации о продукте на складе используется связанная таблица.

### Описание моделей

- **Product**: представляет продукт с полями `title` (название) и `description` (описание).
- **Stock**: представляет склад с полем `address` (адрес) и связью с продуктами через таблицу `StockProduct`.
- **StockProduct**: связующая таблица между продуктами и складами, содержит информацию о количестве и цене продукта на складе.

## Функционал

- **CRUD-операции** для продуктов и складов.
- **Поиск продуктов** по названию и описанию.
- **Поиск складов** по продуктам.
- **Пагинация** для вывода списков.

## Примеры API-запросов

### Базовый URL

`http://localhost:8000/api/v1`

### Продукты

### Создание продукта

```
POST /products/
Content-Type: application/json

{
  "title": "Помидор",
  "description": "Лучшие помидоры на рынке"
}
```

### Получение списка продуктов

```

GET /products/
Content-Type: application/json

```

### Обновление продукта

```

PATCH /products/1/
Content-Type: application/json

{
  "description": "Самые сочные и ароматные помидорки"
}

```

### Удаление продукта

```

DELETE /products/1/
Content-Type: application/json

```

### Поиск продуктов по названию и описанию

```

GET /products/?search=помидор
Content-Type: application/json

```

### Склады

### Создание склада

```

POST /stocks/
Content-Type: application/json

{
  "address": "Джангильна 3",
  "positions": [
    {
      "product": 2,
      "quantity": 250,
      "price": 120.50
    },
    {
      "product": 3,
      "quantity": 100,
      "price": 180
    }
  ]
}

```

### Обновление записей на складе

```

PATCH /stocks/4/
Content-Type: application/json

{
  "positions": [
    {
      "product": 2,
      "quantity": 100,
      "price": 130.80
    },
    {
      "product": 3,
      "quantity": 243,
      "price": 145
    }
  ]
}

```

### Поиск складов по продукту (идентификатор продукта)

```

GET /stocks/?products=3
Content-Type: application/json

```

### Поиск складов по продукту (название или описание продукта)

```

GET /stocks/?search=помид
Content-Type: application/json

```

## Настройки проекта

Для запуска проекта выполните следующие шаги:

1. Установите зависимости:
    
    ```bash
    
    pip install -r requirements.txt
    
    ```
    
2. Создайте базу данных в PostgreSQL и примените миграции:
    
    ```bash
    
    python manage.py migrate
    
    ```
    
3. Запустите сервер разработки:
    
    ```bash
    
    python manage.py runserver
    
    ```
    

## Настройки Django Rest Framework

```python

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
}

```

## Заметки

- В файле `urls.py` настроены маршруты для работы с API.
- Реализована пагинация для списков продуктов и складов.
- В `serializers.py` переопределены методы создания и обновления для обеспечения работы с связанными данными.

```python

# Пример настройки сериализаторов и фильтров
import json
from itertools import product
from django_filters import rest_framework as filters
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['id']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description']

class StockFilter(filters.FilterSet):
    products = filters.NumberFilter(field_name='positions__product__id', lookup_expr='exact')

    class Meta:
        model = Stock
        fields = ['products']

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filterset_class = StockFilter
    search_fields = ['address']
    ordering_fields = ['id']

```

```go
go
Копировать код

Этот `README.md` содержит подробное описание проекта, примеры запросов и инструкции по запуску, что поможет другим разработчикам или пользователям легко разобраться с проектом.

```

### Вы сказали:

Отлично написано, но кнопки скопировать не появилось, видно ты не до конца сгенерировал документ, давай еще раз тоже самое

### ChatGPT сказал:

ChatGPT

Конечно, вот полный `README.md`:

```markdown
markdown
Копировать код
# Склады и товары

## Техническая задача

Реализовать CRUD-логику для продуктов и складов, используя Django Rest Framework (DRF). CRUD — это аббревиатура для Create-Read-Update-Delete, обозначающая базовые операции с сущностями.

## Описание

В рамках проекта реализовано REST API для управления продуктами и складами. Продукты имеют название и описание, а склады хранят информацию о наличии продуктов, их количестве и цене. Для хранения информации о продукте на складе используется связанная таблица.

### Описание моделей

- **Product**: представляет продукт с полями `title` (название) и `description` (описание).
- **Stock**: представляет склад с полем `address` (адрес) и связью с продуктами через таблицу `StockProduct`.
- **StockProduct**: связующая таблица между продуктами и складами, содержит информацию о количестве и цене продукта на складе.

## Функционал

- **CRUD-операции** для продуктов и складов.
- **Поиск продуктов** по названию и описанию.
- **Поиск складов** по продуктам.
- **Пагинация** для вывода списков.

## Примеры API-запросов

### Базовый URL

`http://localhost:8000/api/v1`

### Продукты

#### Создание продукта

```http
POST /products/
Content-Type: application/json

{
  "title": "Помидор",
  "description": "Лучшие помидоры на рынке"
}

```

### Получение списка продуктов

```

GET /products/
Content-Type: application/json

```

### Обновление продукта

```

PATCH /products/1/
Content-Type: application/json

{
  "description": "Самые сочные и ароматные помидорки"
}
```

### Удаление продукта

```

DELETE /products/1/
Content-Type: application/json
```

### Поиск продуктов по названию и описанию

```

GET /products/?search=помидор
Content-Type: application/json
```

### Склады

### Создание склада

```

POST /stocks/
Content-Type: application/json

{
  "address": "Джангильна 3",
  "positions": [
    {
      "product": 2,
      "quantity": 250,
      "price": 120.50
    },
    {
      "product": 3,
      "quantity": 100,
      "price": 180
    }
  ]
}

```

### Обновление записей на складе

```
PATCH /stocks/4/
Content-Type: application/json

{
  "positions": [
    {
      "product": 2,
      "quantity": 100,
      "price": 130.80
    },
    {
      "product": 3,
      "quantity": 243,
      "price": 145
    }
  ]
}
```

### Поиск складов по продукту (идентификатор продукта)

```
GET /stocks/?products=3
Content-Type: application/json
```

### Поиск складов по продукту (название или описание продукта)

```
GET /stocks/?search=помид
Content-Type: application/json
```

## Настройки проекта

Для запуска проекта выполните следующие шаги:

1. Установите зависимости:
    
    ```bash
    pip install -r requirements.txt
    ```
    
2. Создайте базу данных в PostgreSQL и примените миграции:
    
    ```bash
    python manage.py migrate
    ```
    
3. Запустите сервер разработки:
    
    ```bash
    python manage.py runserver
    ```
    

## Настройки Django Rest Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
}
```

## Заметки

- В файле `urls.py` настроены маршруты для работы с API.
- Реализована пагинация для списков продуктов и складов.
- В `serializers.py` переопределены методы создания и обновления для обеспечения работы с связанными данными.

```python
# Пример настройки сериализаторов и фильтров
import json
from itertools import product
from django_filters import rest_framework as filters
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['id']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description']

class StockFilter(filters.FilterSet):
    products = filters.NumberFilter(field_name='positions__product__id', lookup_expr='exact')

    class Meta:
        model = Stock
        fields = ['products']

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filterset_class = StockFilter
    search_fields = ['address']
    ordering_fields = ['id']
```
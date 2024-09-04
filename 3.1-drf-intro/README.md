# Умный дом API

## Описание

Умный дом API — это проект, реализующий REST API для управления данными температурных датчиков. Проект разработан с использованием Django и Django REST Framework и включает операции CRUD (Create, Read, Update, Delete) для работы с датчиками и их измерениями.

### Техническое задание

Система должна поддерживать следующие функции:

1. **Создание датчика**: Указывать название и описание датчика.
2. **Изменение датчика**: Обновлять название и описание датчика.
3. **Добавление измерения**: Указывать ID датчика и температуру при измерении.
4. **Получение списка датчиков**: Выдавать краткую информацию по датчикам (ID, название, описание).
5. **Получение информации по конкретному датчику**: Выдавать полную информацию о датчике, включая список всех измерений с температурой и временем.

Дополнительно:
- Прикрепление изображения к измерению: Датчики могут прикладывать фото к измерениям.

## Установка

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/dm-morozov/Netology_25_Django_homework_1/tree/video/3.1-drf-intro/smart_home.git
    cd smart-home
    ```

2. **Создайте виртуальное окружение и активируйте его:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте базу данных и выполните миграции:**

    Создайте базу данных в PostgreSQL и настройте параметры подключения в `settings.py`. Затем выполните миграции:

    ```bash
    python manage.py migrate
    ```

5. **Создайте суперпользователя для доступа к админке:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Запустите сервер разработки:**

    ```bash
    python manage.py runserver
    ```

7. **Приложение будет доступно по адресу:**

    ```
    http://127.0.0.1:8000/
    ```

## API

### Датчики

- **GET /api/sensors/** - Получить список датчиков
- **POST /api/sensors/** - Создать новый датчик
- **GET /api/sensors/{id}/** - Получить информацию о конкретном датчике
- **PUT /api/sensors/{id}/** - Обновить информацию о датчике
- **PATCH /api/sensors/{id}/** - Частично обновить информацию о датчике
- **DELETE /api/sensors/{id}/** - Удалить датчик

### Измерения

- **GET /api/measurements/** - Получить список измерений
- **POST /api/measurements/** - Создать новое измерение

## Модели

### Sensor

- `name` (CharField): Название датчика
- `description` (CharField): Описание датчика (необязательно)

### Measurement

- `sensor` (ForeignKey): Датчик, к которому относится измерение
- `temperature` (FloatField): Температура
- `created_at` (DateTimeField): Время создания измерения
- `image` (ImageField, optional): Изображение, связанное с измерением

## Сериализаторы

### MeasurementSerializer

Используется для сериализации данных измерений.

```python
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'image', 'created_at']
```

### SensorDetailSerializer

Используется для сериализации данных датчиков и их измерений.

```python
class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

```

## Админка

В административной панели Django доступны следующие модели:

- **Sensor** - Управление датчиками
- **Measurement** - Управление измерениями

### Настройки для медиафайлов

В `settings.py` добавьте настройки для медиафайлов:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')
```

## Документация по проекту

Для запуска проекта выполните следующие шаги:

1. Установите зависимости:
    
    ```bash
    pip install -r requirements.txt
    ```
    
2. Создайте базу данных в PostgreSQL и выполните миграции:
    
    ```bash
    python manage.py migrate
    ```
    
3. Запустите сервер разработки:
    
    ```bash
    python manage.py runserver
    ```
    

## Бэкапы и данные

### Создание резервной копии данных

Для создания резервной копии данных выполните:

```bash
python manage.py dumpdata measurement.Sensor measurement.Measurement --indent 2 > smart_home.json
```

### Восстановление данных

Чтобы загрузить данные из резервной копии, выполните:

```bash
python manage.py loaddata smart_home.json
```

## Примеры запросов

Примеры запросов к API можно просмотреть в файле `requests.http`, который содержит примеры запросов для создания, обновления и получения данных.

## Дополнительные задания

### Прикрепление картинки к измерению

Чтобы добавить возможность прикрепления изображений к измерениям, необходимо обновить модель `Measurement`, добавив поле `ImageField`. Это поле опционально и должно быть добавлено в `Measurement` следующим образом:

```python
class Measurement(models.Model):
    sensor = ForeignKey(Sensor, on_delete=CASCADE, related_name='measurements', verbose_name='Датчик')
    temperature = FloatField(verbose_name='Температура')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Время измерения')
    image = ImageField(blank=True, null=True, upload_to='measurements/', verbose_name='Изображение')
```

Обновите сериализатор `MeasurementSerializer`, чтобы включить поле изображения:

```python
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'image', 'created_at']
```

---

Если у вас есть вопросы или предложения, не стесняйтесь обращаться через [Issues](https://github.com/dm-morozov/Netology_25_Django_homework_1/tree/video/3.1-drf-intro/smart_home/issues).

### Описание элементов README

1. **Описание**: Общее представление о проекте и его функциональности.
2. **Установка**: Пошаговая инструкция по установке и запуску проекта.
3. **API**: Описание доступных API-эндпоинтов.
4. **Модели**: Подробности о моделях данных, используемых в проекте.
5. **Сериализаторы**: Описание сериализаторов, используемых для обработки данных.
6. **Админка**: Информация о доступных моделях в административной панели.
7. **Документация по проекту**: Инструкции для запуска проекта и миграции данных.
8. **Бэкапы и данные**: Как создать резервные копии данных.
9. **Примеры запросов**: Указание на файл с примерами запросов.
10. **Дополнительные задания**: Инструкции по добавлению дополнительного функционала.
11. **Лицензия**: Информация о лицензии проекта.
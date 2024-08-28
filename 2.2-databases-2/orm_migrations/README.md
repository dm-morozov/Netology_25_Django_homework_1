# Руководство по проекту Django "Школа"

## Описание проекта

Этот проект представляет собой систему для управления данными о учениках и учителях школы. Изначально модели были настроены так, что у каждого ученика мог быть только один учитель. Для решения этой проблемы необходимо было изменить модели и сделать связь многие ко многим между учениками и учителями.

## Задание

1. **Поменять отношение моделей:**
    - Измените модели `Student` и `Teacher`, заменив связь ForeignKey на ManyToManyField.
2. **Обновить шаблон списка учеников:**
    - Поправьте шаблон `students_list.html`, чтобы отображать список учителей для каждого ученика с учётом изменений в моделях.
3. **Проверить производительность:**
    - Используйте `prefetch_related` для оптимизации запросов к базе данных и уменьшения числа SQL-запросов.

## Подсказки

1. **Изменение моделей:**
    - Замените `ForeignKey` на `ManyToManyField` в модели `Student`. Обновите название поля с `teacher` на `teachers`.
    - Добавьте параметр `related_name='students'` к полю `ManyToManyField`.
2. **Обновление шаблона:**
    - Для отображения учителей ученика используйте вложенный цикл в шаблоне:
    
    ```html
    {% for teacher in student.teachers.all %}
      <p>{{ teacher.name }}: {{ teacher.subject }}</p>
    {% endfor %}
    
    ```
    
3. **Проверка запросов:**
    - Используйте `django-debug-toolbar` для анализа количества SQL-запросов и оптимизируйте их с помощью `prefetch_related`.
    
    Документация Django по работе с ManyToManyField: [Документация Django](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#working-with-many-to-many-models)
    

## Документация по проекту

### Установка и запуск

1. **Установите зависимости:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
2. **Проведите миграцию базы данных:**
    
    ```bash
    python manage.py migrate
    ```
    
3. **Загрузите тестовые данные:**
    - **Важно:** Загрузите данные до изменения моделей и применения миграций.
    
    ```bash
    python manage.py loaddata school.json
    ```
    
    Если вы изменили модели, но не загрузили тестовые данные, вы можете создать их вручную в админке.
    
4. **Запустите отладочный веб-сервер:**
    
    ```bash
    python manage.py runserver
    ```
    

### Примеры кода

### Вью для отображения списка учеников

```python

from django.views.generic import ListView
from django.shortcuts import render
from .models import Student

def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'
    students = Student.objects.all().order_by(ordering).prefetch_related('teachers')
    context = {'object_list': students}
    return render(request, template, context)

```

### URLs

```python
from django.urls import path
from school.views import students_list
from django.urls import include

urlpatterns = [
    path('', students_list, name='students'),
    path('__debug__/', include('debug_toolbar.urls')),
]

```

### Модели

```python

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=30, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    teachers = models.ManyToManyField(Teacher, verbose_name='Учителя', related_name='students')
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.name

```

### Конфигурация базы данных

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'work_with_database',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': '20145',
    }
}

```

### Настройка Django Debug Toolbar

1. **Установите `django-debug-toolbar`:**
    
    ```bash
    
    pip install django-debug-toolbar
    
    ```
    
2. **Добавьте `debug_toolbar` в `INSTALLED_APPS`:**
    
    ```python

    INSTALLED_APPS = [
        ...
        'debug_toolbar',
        ...
    ]
    
    ```
    
3. **Добавьте `debug_toolbar.middleware.DebugToolbarMiddleware` в `MIDDLEWARE`:**
    
    ```python

    MIDDLEWARE = [
        ...
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        ...
    ]
    
    ```
    
4. **Настройте `INTERNAL_IPS` и `DEBUG_TOOLBAR_CONFIG`:**
    
    ```python

    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
        'INTERCEPT_REDIRECTS': False,
        'SHOW_COLLAPSED': True,
    }
    
    ```
    

### Обновление файла данных

Для создания нового файла данных после изменений в моделях используйте команду:

```bash

python manage.py dumpdata school.Student school.Teacher --indent 2 > school_new.json

```

Загрузите обновленные данные с помощью:

```bash

python manage.py loaddata school_new.json

```

---

Этот файл README содержит все необходимые шаги и примеры кода для работы с проектом, включая установку, настройку и запуск.
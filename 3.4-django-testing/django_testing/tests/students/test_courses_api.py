from pprint import pprint
from tokenize import Triple
from urllib import response

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture()
def student_factory():

    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    
    return factory


@pytest.fixture()
def course_factory():

    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    
    return factory


# Проверка получения первого курса (retrieve-логика)


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    
    # Arrange
    
    # Создаем курсы через фабрику
    course_list = course_factory(_quantity=1)

    # Строим URL для запроса
    url = f"/api/v1/courses/{course_list[0].id}/"

    # Act

    # Строим урл и делаем запрос через тестовый клиент
    response = client.get(url)

    # Assert

    # Проверяем код ответа
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    # print(f"В дате лежит id: {data.get('id')}")
    # print(f"В course лежит id: {course_list[0].id}")
    assert data.get("id") == course_list[0].id
    # print(f"Сравниваем name в дате и в course: {course_list[0].name} == {data.get('name')}")
    assert data.get("name") == course_list[0].name


# Проверка получения списка курсов (list-логика)


@pytest.mark.django_db
def test_get_list_courses(client, course_factory):

    # Arrange
    quantity = 5
    # Создаем несколько курсов через фабрику
    course_list = course_factory(_quantity=quantity)

    # Строим URL для запроса
    url = "/api/v1/courses/"

    # Act

    response = client.get(url)

    # Assert

    assert response.status_code == status.HTTP_200_OK
    
    response_data = response.json()
    # pprint(response_data)
    assert len(response_data) == len(course_list) == quantity
    assert all(course_dict.get('name') in [course.name for course in course_list] 
               for course_dict in response_data)


# Проверка фильтрации списка курсов по id


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):

    # Arrange
    # Создаем несколько курсов через фабрику
    quantity = 5

    # Выбираем один курс для фильтрации по id
    course_target = 2
    
    if course_target >= quantity: course_target = 0
    # course_list = course_factory(_quantity=quantity)
    course = course_factory(_quantity=quantity)[course_target]


    # pprint([{key: value for key, value in course.__dict__.items() 
    #          if not key.startswith('_')} 
    #          for course in course_list])
    

    # Строим URL для запроса
    url = f"/api/v1/courses/?id={course.id}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK

    responce_data = response.json()
    assert len(responce_data) == 1

    assert course.id == responce_data[0].get('id')


# Проверка фильтрации списка курсов по name


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):

    # Arrange
    # Создаем несколько курсов через фабрику
    quantity = 5

    # Выбираем один курс для фильтрации по name

    course_target = course_factory(_quantity=quantity)[0]

    # Строим URL для запроса
    url = f"/api/v1/courses/?name={course_target.name}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    assert course_target.name == response_data[0]['name']


# тест успешного создания курса:
# здесь фабрика не нужна, готовим JSON-данные и создаём курс


@pytest.mark.django_db
def test_create_course(client):

    # Arrange
    # Готовим словать с данными для создания курса

    course_data = [
        {
        'name': "Fullstack-разработчик на Python"
        },
        {
        'name': "Основы Python"
        }
    ]

    # Строим URL для запроса
    url = f"/api/v1/courses/"

    # Act

    for course in course_data:
        response = client.post(path=url, data=course, format='json')
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert course['name'] == response.json()['name']


# тест успешного обновления курса:
# сначала через фабрику создаём, потом обновляем JSON-данными


@pytest.mark.django_db
def test_update_course(client, course_factory):

    # Arrange
    # Создаем курс через фабрику
    course = course_factory(_quantity=1)[0]

    course_updated_data = {
        'name': "Fullstack-разработчик на Python"
        }
    
    # Строим URL для запроса
    url = f"/api/v1/courses/{course.id}/"

    # Act
    response = client.put(path=url, data=course_updated_data, format='json')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == course_updated_data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    course = course_factory()
    url = f"/api/v1/courses/{course.id}/"

    # Act
    response = client.delete(url)
    # Проверяем, что курс действительно удален - делаем к нему запрос
    response_after_delete = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response_after_delete.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize("student_count, is_valid", [
    (12, True),
    (19, True),
    (25, False),
    # (28, True)
    ])
def test_student_limit_on_course(settings, course_factory, 
                                 student_factory, student_count, is_valid):
    
    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 20
    course = course_factory()
    course.save()  # Сохраняем курс, чтобы получить id курсов
    students = student_factory(_quantity=student_count)
    
    # Act
    # Добавляем студентов на курс, удаляя всех старых. Так работает метод set()
    course.students.set(students)

    # Assert
    if is_valid:
        try:
            # Проверяем валидацию
            course.clean()
        except ValidationError:
            pytest.fail(f"Возникла ошибка валидации, при том, что ожидалось, что будет все впорядке." 
                        f"Количество студентов: {student_count}, "
                        f"допустимое количество: {settings.MAX_STUDENTS_PER_COURSE}")
    else:
        # Ожидаем ошибку (число студентов превышает лимит), проверяем, что ошибка возникает
        with pytest.raises(ValidationError):
            # clean должен выдать ValidationError
            course.clean()





from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )


    def clean(self) -> None:
        """Валидация на максимальное количество студентов на курсе"""
        # Проверяем существует ли объект в базе данных 
        # и непревышает ли максимальное количество студентов в группе
        if self.pk and self.students.count() > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f"На курсе не может быть более {settings.MAX_STUDENTS_PER_COURSE} студентов")
        return super().clean()

    
    # Переопределение метода сохранения save()


    def save(self, *args, **kwargs):
        if self.pk:
            self.clean()
        super().save(*args, **kwargs)
    

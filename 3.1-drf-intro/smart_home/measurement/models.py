from email.mime import image
from tabnanny import verbose

from django.db import models
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    ImageField,
)

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = CharField(max_length=50, unique=True, verbose_name='Название')
    description = CharField(max_length=255, blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self) -> str:
        return self.name


class Measurement(models.Model):
    sensor = ForeignKey(Sensor, on_delete=CASCADE, related_name='measurements', verbose_name='Датчик')
    # Температура при изменении
    temperature = FloatField(verbose_name='Температура')
    # Дата и время измерения
    created_at = DateTimeField(auto_now_add=True, verbose_name='Время измерения')
    image = ImageField(blank=True, null=True, upload_to='measurements/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

    def __str__(self) -> str:
        return f"{self.sensor.name}: {self.temperature} в {self.created_at}"

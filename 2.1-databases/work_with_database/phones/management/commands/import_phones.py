import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Импорт данных телефона из файла CSV'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            phone_instance = Phone(
                name = phone.get('name', 'Имя не указано'),
                price = float(phone.get('price', '0')),
                image = phone.get('image', 'Изображение не указано'),
                release_date = phone.get('release_date', '01.01.0001'),
                lte_exists = bool(phone.get('lte_exists', 'False')),
                slug = slugify(phone.get('name', 'Имя не указано'))
            )
            phone_instance.save()

        self.stdout.write(self.style.SUCCESS('Телефоны успешно импортированы!'))
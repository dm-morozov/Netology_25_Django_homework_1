from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
from os import listdir


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.now().strftime('%H:%M:%S')
    msg = f'<strong>Текущее время:</strong> {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    try:
        files = ['<li>' + file_li + '</li>' for file_li in listdir('.')]
    except FileNotFoundError:
        files = ['<p><strong>Рабочая директория пуста</strong></p>']
    finally:
        files_list = ''.join(files)
        msg = f'<h3><strong>Список файлов в рабочей директории:</strong></h3>' \
              f'<ul style="line-height: 1.4;">{files_list}</ul>'
    return HttpResponse(msg)

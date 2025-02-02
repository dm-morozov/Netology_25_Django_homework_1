from django.shortcuts import render, redirect, get_object_or_404
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    phones = Phone.objects.all()

    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')

     
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'

    # Строчка phone = get_object_or_404(Phone, slug=slug) в Django 
    # используется для получения объекта модели Phone по полю slug 
    # из базы данных, при отсутствии объекта возвращается ошибка 404.
    # phone = get_object_or_404(Phone, slug=slug)

    # Другой вариант решения через try-except:
    try:
        phone = Phone.objects.get(slug=slug)
        print(vars(phone))
    except Phone.DoesNotExist:
        return redirect('catalog')
    
    context = {'phone': phone}
    
    return render(request, template, context)

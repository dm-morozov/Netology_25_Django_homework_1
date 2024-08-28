from django.shortcuts import render
from books.models import Book
from django.http import Http404
from django.urls import reverse
from datetime import datetime


def books_view(request):
    books = Book.objects.all().order_by('pub_date')
    # print(vars(books))

    template = 'books/books_list.html'
    context = {
        'books': books,
    }
    return render(request, template, context)

def books_by_date_view(request, pub_date):

    books = Book.objects.filter(pub_date=pub_date)

    # Находим предыдущую и следующую дату выпуск книги
    book_previous_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    book_next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    template = 'books/books_by_date.html'
    
    context = {
        'books': books,
        'previous_date': book_previous_date,
        'next_date': book_next_date
    }

    return render(request, template, context)
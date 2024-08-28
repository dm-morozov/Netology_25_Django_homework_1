from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'

    ordering = '-published_at'
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    articles = Article.objects.all().order_by(ordering).prefetch_related('scopes__tag')


    context = {
        'object_list': articles,
    }

    return render(request, template, context)

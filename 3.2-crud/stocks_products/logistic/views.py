import json
from itertools import product

from django_filters import rest_framework as filters
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filterset_fields = ['id',]
    search_fields = ['title', 'description',]
    ordering_fields = ['id', 'title', 'description']


class StockFilter(filters.FilterSet):
    products = filters.NumberFilter(field_name='positions__product__id', lookup_expr='exact')
    # search = filters.CharFilter(method='filter_by_products_search')

    class Meta:
        model = Stock
        fields = ['products']

    #     fields = ['products', 'search']

    # def filter_by_products_search(self, queryset, name, value):
    #     products = Product.objects.filter(title__icontains = value) | Product.objects.filter(description__icontains = value)
    #     queryset = queryset.filter(positions__product__in=products).distinct()

    #     print(value)
    #     print(products)
    #     print(queryset)
        
    #     return json.dumps(queryset)


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filterset_class = StockFilter
    search_fields = ['address', ]
    ordering_fields = ['id',]
    search_fields = ['products__title','products__description',]
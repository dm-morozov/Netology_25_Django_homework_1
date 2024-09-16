from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices
from django.contrib.auth.models import User

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at']

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import MeasurementView, SensorDetailView, SensorView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorView.as_view(), name='sensors-list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensors-detail'),
    path('measurements/', MeasurementView.as_view(), name='measurements-list'),
  ]
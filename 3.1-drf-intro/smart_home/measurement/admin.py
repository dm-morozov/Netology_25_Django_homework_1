from django.contrib import admin

from .models import Measurement, Sensor

# Register your models here.


class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 1             
    max_num = 1       


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_editable = ['description']
    inlines = [MeasurementInline]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'temperature', 'image', 'created_at']

    def sensor_name(self, obj):
        return obj.sensor.name
    sensor_name.short_description = 'Имя датчика'
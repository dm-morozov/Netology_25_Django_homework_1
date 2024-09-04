from measurement.models import Measurement, Sensor
from rest_framework import serializers

# TODO: опишите необходимые сериализаторы


class MeasurementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'image', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):

    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

        
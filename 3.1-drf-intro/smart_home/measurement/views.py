from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Measurement, Sensor
from .serializers import MeasurementSerializer, SensorDetailSerializer

# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView


# class MeasurementView(APIView):
    
#     def get(self, request):
#         """Получение списка измерений"""
#         measurements = Measurement.objects.all()
#         serializer = MeasurementSerializer(measurements, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class MeasurementView(generics.ListCreateAPIView):

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorView(generics.ListCreateAPIView):

    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class SensorDetailView(generics.RetrieveUpdateAPIView):

    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import (
    Advertisement,
    AdvertisementStatusChoices,
    FavoriteAdvertisement,
)
from advertisements.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyUser
from advertisements.serializers import (
    AdvertisementSerializer,
    FavoriteAdvertisementSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # print(queryset.first().is_staff)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnlyUser()]
        return [IsOwnerOrReadOnlyUser()]


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    # DjangoFilterBackend установлен глобально
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    @action(detail=True, methods=['post'], url_path='t_fav', permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        advertisement = self.get_object()
        user = request.user

        if advertisement.creator == user:
            return Response({'detail': "Нельзя добавлять свое объявление в избранное"}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = FavoriteAdvertisement.objects.get_or_create(user=user, advertisement=advertisement)

        if created:
            serializer = FavoriteAdvertisementSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response({'detail': "Объявление удалено из избранного."}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def favorites(self, request):
        user = request.user
        # print(user)
        favorite_advertisements = Advertisement.objects.filter(favoriteadvertisement__user=user)

        serializer = self.get_serializer(favorite_advertisements, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        """
        Фильтрация объявлений:
        зарегестрированные пользователи видят
        только свои объявления в статусе DRAFT
        или все объявления со статусом OPEN.
        Незарегестрированные пользователи
        видят объявления со статусом OPEN
        """
        user = self.request.user
        # print(user.is_authenticated)

        if user.is_authenticated:
            return Advertisement.objects.filter(
                creator=user
            ) | Advertisement.objects.filter(
                status=AdvertisementStatusChoices.OPEN)

        return Advertisement.objects.filter(status=AdvertisementStatusChoices.OPEN)
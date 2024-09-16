from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import serializers

from advertisements.models import (
    Advertisement,
    AdvertisementStatusChoices,
    FavoriteAdvertisement,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_field = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        user = self.context['request'].user
        open_adv_count = Advertisement.objects.filter(
            creator=user, status=AdvertisementStatusChoices.OPEN).count()

        # print(f"{user}: {open_adv_count}")
        # print(data.get('status'))
        # print(self.context['request'])

        if data.get('status') == AdvertisementStatusChoices.OPEN and open_adv_count >= 10:
            raise serializers.ValidationError(
                "У вас уже есть 10 открытых объявлений. Для продолжения закройте любое объявление и повторите операцию.")

        return data

    def to_representation(self, instance):
        """Метод для вывода данных. Фильтрация черновика"""

        # Показывает объявления "Черновик" только их создателю.

        # print(instance.__dict__)
        # print(vars(instance))
        # print(model_to_dict(instance))
        request = self.context['request']


        # Это словарь с полями, которые были указаны в сериализаторе.
        represention = super().to_representation(instance)
        # print(represention)

        user = request.user
        # print(user)

        if instance.status == AdvertisementStatusChoices.DRAFT and instance.creator != user:
            return None # Не показывать объявления если статус черновик и пользователь не создатель

        return represention

class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAdvertisement
        fields = ['id', 'user', 'advertisement']
        read_only_fields = ['user']

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super.create(validated_data)

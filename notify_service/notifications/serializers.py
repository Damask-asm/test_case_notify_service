from rest_framework import serializers

from .channels import CHANNEL_CHOICES
from .models import UserNotification



class NotificationRequestSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()
    message = serializers.CharField()
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=CHANNEL_CHOICES),
        required=False,         # ← необязательно указывать
        allow_empty=True        # ← пустой список тоже ок
    )

    def validate_external_id(self, value):
        if not UserNotification.objects.filter(external_id=value).exists():
            raise serializers.ValidationError("Пользователь с таким external_id не найден.")
        return value

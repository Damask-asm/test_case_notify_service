from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .permissions import HasValidApiKey
from .serializers import NotificationRequestSerializer
from .models import UserNotification
from .tasks import send_notification_task

@extend_schema(
    request=NotificationRequestSerializer,
    responses={
        202: OpenApiResponse(description="Задача поставлена в очередь"),
        400: OpenApiResponse(description="Ошибочные данные"),
    },
    tags=["Notifications"],
    description="Создаёт задачу на отправку уведомления пользователю через один или несколько каналов."
)
class NotificationSendView(APIView):
    permission_classes = [HasValidApiKey]
    def post(self, request):
        serializer = NotificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        external_id = validated['external_id']
        message = validated['message']
        user = UserNotification.objects.get(external_id=external_id)

        # если каналы не заданы — подставляем по приоритету
        channels = validated.get('channels')
        if not channels:
            channels = []
            if user.email:
                channels.append('email')
            if user.telegram_id:
                channels.append('telegram')
            if user.phone:
                channels.append('sms')

            if not channels:
                return Response({
                    'error': 'У пользователя не указан ни один контактный канал.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Отправляем задачу в Celery
        task = send_notification_task.delay(user.id, message, channels)

        return Response({
            'status': 'Задача поставлена в очередь',
            'task_id': task.id,
            'channels': channels,
        }, status=status.HTTP_202_ACCEPTED)
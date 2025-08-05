from django.urls import path
from .views import NotificationSendView

urlpatterns = [
    path('send/', NotificationSendView.as_view(), name='send_notification'),
]

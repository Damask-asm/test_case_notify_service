import secrets

from django.db import models

from .channels import CHANNEL_CHOICES


class UserNotification(models.Model):
    external_id = models.BigIntegerField(unique=True, blank=True, null=True)  # Внешний ID из другого сервиса. CRM, например

    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} (ID {self.id})"


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('success', 'Успешно'),
        ('failed', 'Ошибка'),
        ('unavailable', 'Канал недоступен'),
    ]

    user = models.ForeignKey(UserNotification, on_delete=models.CASCADE, related_name='notifications')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"User: {self.user.full_name} message: {self.message} ({self.status})"


class ApiKey(models.Model):
    key = models.CharField(max_length=128, unique=True)
    label = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)  # 64 символа = безопасно
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.key[:8]}...)"

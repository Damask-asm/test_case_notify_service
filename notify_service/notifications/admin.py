from django.contrib import admin
from .models import UserNotification, NotificationLog, ApiKey


@admin.register(UserNotification)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'telegram_id')
    search_fields = ('full_name', 'email', 'phone', 'telegram_id')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'channel', 'status', 'created_at', 'sent_at')
    list_filter = ('channel', 'status')
    search_fields = ('user__full_name', 'message', 'error_message')
    readonly_fields = ('created_at', 'sent_at', 'error_message')


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('label', 'key_short', 'is_active', 'created_at')
    search_fields = ('label', 'key')
    readonly_fields = ('created_at',)
    list_filter = ('is_active',)

    def key_short(self, obj):
        return obj.key[:10] + "…" if len(obj.key) > 12 else obj.key
    key_short.short_description = "API-ключ"
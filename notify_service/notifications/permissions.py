from rest_framework.permissions import BasePermission
from .models import ApiKey

class HasValidApiKey(BasePermission):
    def has_permission(self, request, view):
        auth_key = request.headers.get('X-API-Key')
        if not auth_key:
            return False
        return ApiKey.objects.filter(key=auth_key, is_active=True).exists()

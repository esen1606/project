from rest_framework import permissions
from .models import Article

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.visibility == Article.PUBLIC:
                return True
            if obj.visibility == Article.PRIVATE and request.user.is_authenticated and request.user.role == 'subscriber':
                return True
        return obj.author == request.user

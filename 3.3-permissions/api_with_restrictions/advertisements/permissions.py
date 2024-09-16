from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return request.user == obj.creator


class IsOwnerOrReadOnlyUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return request.user == obj
from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    '''Доступ владелец или модер'''
    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ владельцу объекта
        if obj.owner == request.user:
            return True

        # Разрешаем доступ модераторам
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    '''Доступ владелец'''
    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ владельцу объекта
        if obj.owner == request.user:
            return True

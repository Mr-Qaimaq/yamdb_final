from rest_framework import permissions


class AdminModifyOrReadOnlyPermission(permissions.BasePermission):
    """
    Только у админа есть доступ для
    редактирования или только для получения данных.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_admin:
            return True


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['get_me', 'update_me', 'delete_me']:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        if view.action in ['get_me', 'update_me', 'delete_me']:
            return obj.author == request.user
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.is_admin)


class ReviewAndComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' or view.action == 'create':
            return not request.user.is_anonymous()

        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author
                    or request.user.is_admin
                    or request.user.is_moderator)

        if request.method in permissions.SAFE_METHODS:
            return True
        return False

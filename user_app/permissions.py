from rest_framework import permissions


class AuthorizationPermission(permissions.BasePermission):
    message = 'Accessing other users details not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.user.email != str(obj):
            return False
        return True

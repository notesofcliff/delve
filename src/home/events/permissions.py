from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # only allow for the owner of the object.
        return obj.user == request.user

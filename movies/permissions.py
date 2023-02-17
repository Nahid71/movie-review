from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the movie
        return obj.creator == request.user

class IsInappropriateOrAuthorOnly(permissions.BasePermission):
    """
    Custom permission for hidding movie object if inappropriate and only author can see.
    """

    def has_object_permission(self, request, view, obj):
        # if request by author then  show the object
        if obj.creator == request.user:
            return True
        # if 'is_inappropriate' is True then hide the object
        if obj.is_inappropriate:
            return False
        return True

        # Write permissions are only allowed to the creator of the movie
        return obj.creator == request.user
    
class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superAdmin access the object.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

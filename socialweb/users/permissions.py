from rest_framework import permissions

#  Ограничение - только этот пользователь или администратор
class IsOnlyUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
 
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
 
        # Write permissions are only allowed to the owner of the snippet.
        return obj.username == request.user.username or bool(request.user and request.user.is_staff)


class IsOnlyUserPhotoOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
     
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return obj.user == request.user

class IsOnlyTo_User(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
     
        return obj.to_user == request.user 
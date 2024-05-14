from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj) 
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'admin'))
    

from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    will create a custom permision that allows only admins to access
    a particular view that inherits this, i will consider admin role,
    active user, and whether user is authenticated. This will return a 
    boolean
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_admin()
    

class IsUser(permissions.BasePermission):
   # same idea for user, to add additional security
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_user()
    

class AssignedUser(permissions.BasePermission):
    #for users to update a task
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user
    
class Admin_or_Assigned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        return obj.task.assigned_to == request.user
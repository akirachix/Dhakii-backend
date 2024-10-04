from rest_framework.permissions import BasePermission

class IsAuthenticatedAndHasPermission(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        return True

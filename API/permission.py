from rest_framework.permissions import BasePermission

class IsDirectorOrReadOnly(BasePermission):
    """
    Permite acceso completo a Directores; Consultores solo pueden leer.
    """
    def has_permission(self, request, view):
        # Solo GET está permitido para todos
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Acceso completo si el usuario pertenece al grupo 'Director'
        return request.user.groups.filter(name='Director').exists()

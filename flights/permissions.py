from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite solo a administradores modificar, otros solo lectura.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite a los usuarios modificar solo sus propios objetos, o admin todo.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        # Para reservas y boletos, el dueño es el pasajero vinculado al user
        if hasattr(obj, 'pasajero') and hasattr(obj.pasajero, 'user'):
            return obj.pasajero.user == request.user
        return False

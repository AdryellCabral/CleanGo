from rest_framework.permissions import BasePermission

super_methods = ["PUT","POST","DELETE"]

class IsCustomerOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    if request.method in super_methods:
        return request.user.is_staff
    else: 
      return True
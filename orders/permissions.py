from rest_framework.permissions import BasePermission
import ipdb

super_methods = ["PUT", "POST", "DELETE"]


class IsCustomerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        ipdb.set_trace()
        if request.method in super_methods:
            return request.user.is_staff
        else:
            return True

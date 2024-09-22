from rest_framework import permissions

class IsOwnerOrContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.contributors.all()
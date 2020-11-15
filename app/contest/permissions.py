from rest_framework import permissions
from core.models import UserContest


# TODO: Check if this can be moved to 'core' app
class IsAllowedInContest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserContest.objects.filter(user_id=request.user.id,
                                          contest_id=obj.id
                                          ).count() > 0

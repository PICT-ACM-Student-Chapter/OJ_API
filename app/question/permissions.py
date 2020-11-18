from rest_framework import permissions

from core.models import UserContest


class IsQuestionAllowed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserContest.objects.filter(user_id=request.user.id,
                                          contest_id=obj.contest_id
                                          ).count() > 0

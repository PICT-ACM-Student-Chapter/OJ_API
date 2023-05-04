import datetime

import pytz
from rest_framework import permissions

from core.models import UserContest


class IsAllowedInContest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserContest.objects.filter(user_id=request.user.id,
                                          contest_id=obj.id
                                          ).count() > 0


class IsInTime(permissions.BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        return UserContest.objects.filter(
            contest_id__id=view.kwargs['id'],
            contest_id__start_time__lte=curr_time,
            contest_id__end_time__gte=curr_time
            # status == 'STARTED' or not is handled in the serializer
            # questions are sent only when status is 'STARTED'
        ).count() > 0


class IsStartInTime(permissions.BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        return UserContest.objects.filter(
            contest_id__id=view.kwargs['id'],
            contest_id__start_time__lte=curr_time,
            contest_id__end_time__gte=curr_time,
            status='REGISTERED'
        ).count() > 0

import datetime

import pytz
from rest_framework import permissions

from contest.models import Contest
from core.models import UserContest


# TODO: Check if this can be moved to 'core' app
class IsAllowedInContest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserContest.objects.filter(user_id=request.user.id,
                                          contest_id=obj.id
                                          ).count() > 0


# TODO: Derive from base IsInTime class
class IsInTime(permissions.BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        return Contest.objects.filter(id=view.kwargs['id'],
                                      start_time__lte=curr_time,
                                      end_time__gte=curr_time
                                      ).count() > 0

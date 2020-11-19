import datetime

import pytz
from rest_framework import permissions

from contest.models import Contest
from core.models import UserContest


class IsQuestionAllowed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserContest.objects.filter(user_id=request.user.id,
                                          contest_id__in=obj.contests.all()
                                          ).count() > 0


class IsInTime(permissions.BasePermission):
    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        return Contest.objects.filter(questions__id=view.kwargs['que_id'],
                                      start_time__lte=curr_time,
                                      end_time__gte=curr_time
                                      ).count() > 0

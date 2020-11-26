import datetime

import pytz
from core.models import UserContest
from rest_framework import permissions


class IsRunSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsRunInTime(permissions.BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        # Allow run if any contest a user is registered for is running
        return UserContest.objects.filter(
            user_id=request.user.id,
            contest_id__start_time__lte=curr_time,
            contest_id__end_time__gte=curr_time,
            status='STARTED'
        ).count() > 0


class IsSubmissionInTime(permissions.BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.datetime.now(tz=pytz.UTC)
        # Allow run if any contest a user is registered for is running

        ques_id = view.kwargs['ques_id']
        contest_id = view.kwargs['contest_id']

        return UserContest.objects.filter(
            user_id=request.user.id,
            contest_id__id=contest_id,
            contest_id__questions__id=ques_id,
            contest_id__start_time__lte=curr_time,
            contest_id__end_time__gte=curr_time,
            status='STARTED'
        ).count() > 0

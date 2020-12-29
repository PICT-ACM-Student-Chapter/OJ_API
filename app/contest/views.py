# Create your views here.
from functools import cmp_to_key

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from contest.models import Contest
from contest.permissions import IsAllowedInContest, IsInTime, IsStartInTime
from contest.serializers import LeaderBoardSerializer
from contest.serializers import UserContestSerializer, ContestSerializer
from core.models import UserContest


class ContestList(ListAPIView):
    serializer_class = UserContestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserContest.objects.filter(user_id=self.request.user.id)


class ContestDetails(RetrieveAPIView):
    serializer_class = ContestSerializer
    lookup_url_kwarg = 'id'
    queryset = Contest.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAllowedInContest,
                          IsInTime]


class StartContest(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStartInTime]

    def patch(self, request, id):
        try:
            user_contest = UserContest.objects.get(
                contest_id=id,
                user_id=request.user.id)
            user_contest.status = "STARTED"
            user_contest.save()
            return JsonResponse(UserContestSerializer(user_contest).data)
        except UserContest.DoesNotExist:
            return HttpResponse(status=404)


def compare_scores(a, b):
    """
    return a negative value (< 0) when the left item should be sorted before
    the right item
    return a positive value (> 0) when the left item should be sorted after
    the right item
    """
    if a.total_score > b.total_score:
        return -1
    elif a.total_score < b.total_score:
        return 1
    else:
        if a.total_penalty < b.total_penalty:
            return -1
        else:
            return 1


class LeaderBoard(ListAPIView):
    serializer_class = LeaderBoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contest_id = self.kwargs['contest_id']
        data = UserContest.objects.filter(contest_id__id=contest_id,
                                          status='STARTED')
        return sorted(data, key=cmp_to_key(compare_scores))

    def get(self, request, *args, **kwargs):
        res = cache.get('leaderboard_{}'.format(self.kwargs['contest_id']))
        if not res:
            res = self.list(request, *args, **kwargs).data
            cache.set('leaderboard_{}'.format(self.kwargs['contest_id']), res,
                      settings.CACHE_TTLS['LEADERBOARD'])
        return Response(data=res)

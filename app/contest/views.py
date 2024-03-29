# Create your views here.
from functools import cmp_to_key

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from contest.models import Contest
from contest.permissions import IsAllowedInContest, IsInTime, IsStartInTime
from contest.serializers import LeaderBoardSerializer, \
    UserContestListSerializer, QuestionIdListSerializer
from contest.serializers import UserContestSerializer, ContestSerializer
from core.models import UserContest


class ContestList(ListAPIView):
    serializer_class = UserContestListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

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

        cache_key = 'leaderboard_{}'.format(
            self.kwargs['contest_id'],
        )
        data = cache.get(cache_key)
        if not data:
            data = UserContest.objects.filter(contest_id__id=contest_id,
                                              status='STARTED')
            data = sorted(data, key=cmp_to_key(compare_scores))
            cache.set(cache_key, data,
                      settings.CACHE_TTLS['LEADERBOARD'])
        else:
            self.check_permissions(self.request)
        return data

    def get(self, request, *args, **kwargs):
        res = self.list(self, request, *args, **kwargs)
        cache_key = 'leaderboard_{}_ques'.format(
            self.kwargs['contest_id'],
        )
        ques_ids = cache.get(cache_key)
        if not ques_ids:
            try:
                ques = Contest.objects.get(
                    id=self.kwargs['contest_id']).questions.all()
                ques_ids = QuestionIdListSerializer(ques, many=True).data
                cache.set(cache_key, ques_ids,
                          settings.CACHE_TTLS['CONTEST_QUESTIONS'])
            except Contest.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
        data = res.data
        data['questions'] = ques_ids
        return Response(data=data)

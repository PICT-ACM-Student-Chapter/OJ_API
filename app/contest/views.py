# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from contest.models import Contest
from contest.permissions import IsAllowedInContest, IsInTime
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
    permission_classes = [permissions.IsAuthenticated, IsInTime]

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

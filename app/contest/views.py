# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from contest.models import Contest
from contest.permissions import IsAllowedInContest
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
    permission_classes = [permissions.IsAuthenticated, IsAllowedInContest]

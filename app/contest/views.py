# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView

from contest.models import Contest
from contest.serializers import UserContestSerializer, ContestSerializer
from core.models import UserContest


class ContestList(ListAPIView):
    serializer_class = UserContestSerializer

    def get_queryset(self):
        return UserContest.objects.filter(user_id=self.request.user.id)


class ContestDetails(RetrieveAPIView):
    serializer_class = ContestSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        if UserContest.objects.filter(
                user_id=self.request.user.id,
                contest_id=self.kwargs['id']).count() > 0:
            return Contest.objects.all()

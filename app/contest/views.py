# Create your views here.
from rest_framework.generics import ListAPIView

from contest.serializers import ContestSerializer
from core.models import UserContest


class Contests(ListAPIView):
    serializer_class = ContestSerializer

    def get_queryset(self):
        return UserContest.objects.filter(user_id=self.request.user.id)

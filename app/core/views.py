import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contest.serializers import UserContestSerializer
from core.models import Language, UserContest
from core.serializers import LanguageSerializer


class LanguageList(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = ()

    @method_decorator(cache_page(settings.CACHE_TTLS['LANGS']))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserContestRetrieve(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = UserContestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserContest.objects.filter(user_id=self.request.user)


class ServerTime(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({"time": now})


class Version(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to='/swagger')

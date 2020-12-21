import datetime


from core.models import Language
from core.serializers import LanguageSerializer
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Language
from core.serializers import LanguageSerializer
from core.serializers import UserRegisterSerializer, UserSafeInfoSerializer


class LanguageList(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = ()

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ServerTime(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({"time": now})


class Version(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to='/swagger')

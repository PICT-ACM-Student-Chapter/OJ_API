import datetime

from core.models import Language
from core.serializers import LanguageSerializer
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


class LanguageList(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ServerTime(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({"time": now})


class Version(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"version": settings.VERSION})

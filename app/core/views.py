import datetime

from django.conf import settings
from django.http import JsonResponse
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


class ServerTime(APIView):
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({"time": now})


class Version(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"version": settings.VERSION})


# Create your views here.

class Register(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)


class UserProfile(RetrieveAPIView):
    serializer_class = UserSafeInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = UserSafeInfoSerializer(request.user)
        return JsonResponse(user.data)

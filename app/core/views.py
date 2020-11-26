import datetime

from core.models import Language
from core.serializers import LanguageSerializer
from core.serializers import UserRegisterSerializer, UserSafeInfoSerializer
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


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

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return Response({"version": settings.VERSION})


# Create your views here.

class Register(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)


class UserProfile(RetrieveAPIView):
    serializer_class = UserSafeInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = UserSafeInfoSerializer(request.user)
        return JsonResponse(user.data)

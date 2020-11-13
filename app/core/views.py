# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from core.serializers import UserRegisterSerializer, UserSafeInfoSerializer
# Create your views here.


class Register(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny, )


class UserProfile(RetrieveAPIView):
    serializer_class = UserSafeInfoSerializer
    permission_classes = (permissions.IsAuthenticated, )









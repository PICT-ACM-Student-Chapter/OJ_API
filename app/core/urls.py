from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import Register, UserProfile
from .views import LanguageList, ServerTime, Version

urlpatterns = [
    path(
        "api-auth/", include("rest_framework.urls")
    ),
    path('auth/register', Register.as_view()),
    path('auth/login', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('userProfile', UserProfile.as_view()),
    path('languages/', LanguageList.as_view(), name='lang-list'),
    path('time/', ServerTime.as_view(), name='server-time'),
    path('', Version.as_view(), name='version'),
]

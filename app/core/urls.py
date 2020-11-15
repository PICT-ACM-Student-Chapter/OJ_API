from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import Register, UserProfile

urlpatterns = [
    path('api/auth/register', Register.as_view()),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/userProfile', UserProfile.as_view()),
]

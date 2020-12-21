from django.urls import path, include

from core.views import Register, UserProfile
from .views import LanguageList, ServerTime, Version

urlpatterns = [
    path('languages/', LanguageList.as_view(), name='lang-list'),
    path('time/', ServerTime.as_view(), name='server-time'),
    path('', Version.as_view(), name='version'),
]

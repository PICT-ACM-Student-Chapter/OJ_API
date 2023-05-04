from django.urls import path

from .views import LanguageList, ServerTime, Version, UserContestRetrieve

urlpatterns = [
    path('languages/', LanguageList.as_view(), name='lang-list'),
    path('user-contests/<int:id>', UserContestRetrieve.as_view()),
    path('time/', ServerTime.as_view(), name='server-time'),
    path('', Version.as_view(), name='version'),
]

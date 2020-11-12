from django.urls import path

from contest.views import ContestList, ContestDetails

urlpatterns = [
    path(r'/<int:id>', ContestDetails.as_view()),
    path(r'/', ContestList.as_view()),
]

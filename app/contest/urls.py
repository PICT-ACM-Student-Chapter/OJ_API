from django.urls import path

from contest.views import ContestList, ContestDetails, StartContest

urlpatterns = [
    path(r'/', ContestList.as_view()),
    path(r'/<int:id>', ContestDetails.as_view()),
    path(r'/<int:id>/start', StartContest.as_view()),
]

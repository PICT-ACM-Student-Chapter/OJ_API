from contest.views import ContestList, ContestDetails, StartContest
from django.urls import path
from submission.views import Submit

urlpatterns = [
    path('/<int:id>/start', StartContest.as_view()),
    path('/<int:id>', ContestDetails.as_view()),
    path('/<int:contest_id>/questions/<int:ques_id>/submit', Submit.as_view()),
    path('', ContestList.as_view()),
]

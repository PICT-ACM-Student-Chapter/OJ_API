from contest.views import ContestList, ContestDetails, StartContest
from django.urls import path
from submission.views import SubmissionStatus, Submit, SubmissionList

urlpatterns = [
    path('<int:id>/start', StartContest.as_view()),
    path('<int:id>', ContestDetails.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/submit',
         Submit.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/submit/<int:id>',
         SubmissionStatus.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/submissions',
         SubmissionList.as_view()),

    path('', ContestList.as_view()),
]

from django.urls import path

from contest.views import ContestList, ContestDetails, StartContest, \
    LeaderBoard
from question.views import QuestionList
from submission.views import SubmissionStatus, Submit, SubmissionList, RunRC, \
    CheckRunStatus

urlpatterns = [
    path('<str:id>/start', StartContest.as_view()),
    path('<str:id>', ContestDetails.as_view()),
    path('<str:contest_id>/questions', QuestionList.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/submit', Submit.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/rc/run',
         RunRC.as_view()),  # only for rc
    path('<str:contest_id>/questions/<str:ques_id>/rc/run/<int:id>',
         CheckRunStatus.as_view()),  # only for rc
    #     path('<str:contest_id>/questions/<str:ques_id>/hack/run/<int:id>', ),



    path('<str:contest_id>/questions/<str:ques_id>/submit/<int:id>',
         SubmissionStatus.as_view()),
    path('<str:contest_id>/questions/<str:ques_id>/submissions',
         SubmissionList.as_view()),
    path('<str:contest_id>/leaderboard', LeaderBoard.as_view()),
    path('', ContestList.as_view()),
]

from django.urls import path

from .views import Run, CheckRunStatus, CallbackRunNow, \
    CallbackSubmission, Submit, SubmissionStatus, SubmissionList

urlpatterns = [
    path('run', Run.as_view()),
    path('run/<int:id>', CheckRunStatus.as_view()),
    path('run/callback/<int:sub_id>', CallbackRunNow.as_view()),
    path('submit/<int:id>', SubmissionStatus.as_view()),
    path('submissions/<int:ques_id>', SubmissionList.as_view()),
    path('submit/callback/<int:verdict_id>', CallbackSubmission.as_view())
]

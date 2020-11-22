from django.urls import path

from .views import Run, CheckRunStatus, CallbackRunNow, \
    CallbackSubmission, Submit

urlpatterns = [
    path('run', Run.as_view()),
    path('run/<int:id>', CheckRunStatus.as_view()),
    path('run/callback', CallbackRunNow.as_view()),
    path('submit', Submit.as_view()),
    path('submit/callback', CallbackSubmission.as_view())
]

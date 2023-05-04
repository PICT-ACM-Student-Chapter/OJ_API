from django.urls import path

from .views import Run, CheckRunStatus, CallbackRunNow, \
    CallbackSubmission

urlpatterns = [
    path('run', Run.as_view()),
    path('run/<int:id>', CheckRunStatus.as_view()),
    path('callback/run/<int:sub_id>', CallbackRunNow.as_view()),
    path('callback/submit/<int:verdict_id>', CallbackSubmission.as_view())
]

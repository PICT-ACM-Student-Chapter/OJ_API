from django.urls import path

from submission.views import Run, CheckRunStatus, CallbackRunNow

urlpatterns = [
    path('run', Run.as_view()),
    path('run/<int:id>', CheckRunStatus.as_view()),
    path('run/callback', CallbackRunNow.as_view())
]

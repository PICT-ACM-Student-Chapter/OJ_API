from django.urls import path, include

from contest.views import ContestList, ContestDetails, StartContest

urlpatterns = [
    path('/<int:id>/start', StartContest.as_view()),
    path('/<int:id>', ContestDetails.as_view()),
    path('', ContestList.as_view()),
    path('/<int:contest_id>/questions', include('question.urls'))
]

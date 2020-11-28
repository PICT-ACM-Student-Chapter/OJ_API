from django.urls import path

from question.views import QuestionsList

urlpatterns = [
    path('<int:que_id>', QuestionsList.as_view())
]

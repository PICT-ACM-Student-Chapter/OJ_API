from django.urls import path

from question.views import QuestionsList

urlpatterns = [
    path('<str:que_id>', QuestionsList.as_view())
]

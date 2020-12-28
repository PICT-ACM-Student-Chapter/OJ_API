from django.urls import path

from question.views import QuestionDetail

urlpatterns = [
    path('<str:que_id>', QuestionDetail.as_view())
]

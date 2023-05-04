from django.urls import path

from question.views import BugoffQuestion, QuestionDetail

urlpatterns = [
    path('<str:que_id>', QuestionDetail.as_view()),
    path('<str:que_id>/<str:code_lang>', BugoffQuestion.as_view())
]

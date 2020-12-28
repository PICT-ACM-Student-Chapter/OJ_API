# Create your views here.
from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView, ListAPIView

from core.models import UserQuestion
from question.models import Question, Testcase
from question.permissions import IsQuestionAllowed, IsInTime
from question.serializers import QuestionDetailSerializer, \
    UserQuestionListSerializer


class QuestionDetail(RetrieveAPIView):
    serializer_class = QuestionDetailSerializer
    lookup_url_kwarg = 'que_id'
    lookup_field = 'id'
    permission_classes = [IsQuestionAllowed, IsInTime]

    def get_queryset(self):
        return Question.objects.all().prefetch_related(
            Prefetch('test_cases',
                     queryset=Testcase.objects.filter(is_public=True))
        )


class QuestionList(ListAPIView):
    serializer_class = UserQuestionListSerializer

    def get_queryset(self):
        return Question.objects.filter(
            contests__contest_id=self.kwargs['contest_id']
        )

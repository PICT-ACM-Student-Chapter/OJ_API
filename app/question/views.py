# Create your views here.
from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView

from question.models import Question, Testcase
from question.permissions import IsQuestionAllowed
from question.serializers import QuestionSerializer


class QuestionsList(RetrieveAPIView):
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'que_id'
    lookup_field = 'id'
    permission_classes = [IsQuestionAllowed]

    def get_queryset(self):
        return Question.objects.all().prefetch_related(
            Prefetch('test_cases',
                     queryset=Testcase.objects.filter(is_public=True))
        )

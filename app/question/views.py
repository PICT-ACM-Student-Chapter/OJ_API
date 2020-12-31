# Create your views here.
from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView, ListAPIView

from question.models import Question, Testcase
from question.permissions import IsQuestionAllowed, IsInTime, \
    IsQuestionListInTime
from question.serializers import QuestionDetailSerializer, \
    QuestionListSerializer


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

    @method_decorator(cache_page(settings.CACHE_TTLS['QUESTION_DETAIL']))
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)


class QuestionList(ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = [IsQuestionListInTime]
    pagination_class = None

    def get_queryset(self):
        que_list = cache.get('contest-{}-questions'
                             .format(self.kwargs['contest_id']))

        if not que_list:
            que_list = Question.objects.filter(
                contests__id=self.kwargs['contest_id']
            )
            cache.set('contest-{}-questions'
                      .format(self.kwargs['contest_id']),
                      que_list,
                      settings.CACHE_TTLS['CONTEST_QUESTIONS'])

        return que_list

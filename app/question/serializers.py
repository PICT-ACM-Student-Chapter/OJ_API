from rest_framework import serializers

from question.models import Question, Testcase
from core.models import UserQuestion


class TestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testcase
        fields = ['id', 'input', 'output']


class QuestionDetailSerializer(serializers.ModelSerializer):
    test_cases = TestcaseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'input_format', 'output_format',
                  'constraints', 'test_cases', 'score', ]


class QuestionListSerializer(serializers.ModelSerializer):
    def get_user_score(self, model):
        user_ques = UserQuestion.objects.filter(
            user_contest__contest_id=self.context.kwargs['contest_id'],
            user_contest__user_id=self.context.request.user,
            que_id=model.id
        )
        print(user_ques)
        return user_ques.first().score if user_ques.exists() else 0

    user_score = serializers.SerializerMethodField(read_only=True)

    model = Question
    fields = ['id', 'name', 'score', 'user_score']


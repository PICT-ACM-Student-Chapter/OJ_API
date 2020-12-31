from rest_framework import serializers

from core.models import UserQuestion
from question.models import Question, Testcase


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
            user_contest__contest_id=self.context['view'].kwargs['contest_id'],
            user_contest__user_id=self.context['request'].user,
            que_id=model.id
        )
        try:
            q = user_ques.first()
            user_score = {
                'score': q.score,
                'penalty': q.penalty
            }
        except AttributeError:
            user_score = {
                'score': 0,
                'penalty': 0
            }
        return user_score

    user_score = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'score', 'user_score']

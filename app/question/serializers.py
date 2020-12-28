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
    model = Question
    fields = ['id', 'name', 'score']


class UserQuestionListSerializer(serializers.ModelSerializer):
    que = QuestionListSerializer(many=True, read_only=True)
    user_score = serializers.FloatField(source='score')
    user_penalty = serializers.FloatField(source='penalty')

    class Meta:
        model = UserQuestion
        fields = ['que', 'user_score', 'user_penalty']

from rest_framework import serializers

from question.models import Question, Testcase


class TestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testcase
        fields = ['id', 'input', 'output']


class QuestionSerializer(serializers.ModelSerializer):
    test_cases = TestcaseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'input_format', 'output_format',
                  'constraints', 'test_cases', 'score', ]

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
            user_contest__contest_id=self.context['view'].kwargs['contest_id'],
            user_contest__user_id=self.context['request'].user,
            que_id=model.id
        )
        user_score = {
            'score': user_ques.first().score if user_ques.exists() else 0,
            'penalty': user_ques.first().penalty if user_ques.exists() else 0
        }
        return user_score

    user_score = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'score', 'user_score']


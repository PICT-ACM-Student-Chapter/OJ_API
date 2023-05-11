from rest_framework import serializers

from contest.models import ContestQue
from core.models import UserQuestion
from question.models import IncorrectCode, Question, Testcase


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

class HackingQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IncorrectCode
        fields = ['question', 'incorrect_code', 'code_lang']
class ContestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestQue
        fields = ['is_binary', 'is_reverse_coding', 'is_bugoff', 'order']


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

    def get_contest_que(self, model):
        contest_que = ContestQue.objects.get(
            contest_id=self.context['view'].kwargs['contest_id'],
            question_id=model.id
        )

        return ContestQuestionSerializer(contest_que).data

    user_score = serializers.SerializerMethodField(read_only=True)
    contest_que = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'score', 'user_score', 'contest_que']

from django.db.models import Sum
from rest_framework import serializers

from contest.models import Contest, ContestQue
from core.models import UserContest
from core.models import UserQuestion
from core.serializers import UserSafeInfoSerializer
from question.models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'name', 'score']


class ContestQueSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(read_only=True)

    class Meta:
        model = ContestQue
        fields = ['order', 'question', 'is_reverse_coding', 'is_binary']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     que_repr = representation.pop('question')
    #     for key in que_repr:
    #         representation[key] = que_repr[key]
    #     return representation


class ContestSerializer(serializers.ModelSerializer):

    def get_user_score(self, model):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        user_contest = UserContest.objects.filter(user_id=user,
                                                  contest_id=model.id).first()
        user_ques = UserQuestion.objects.filter(user_contest=user_contest)
        total_sum = user_ques.aggregate(Sum('score'))
        return total_sum['score__sum'] or 0

    def get_max_score(self, model):
        questions = model.questions
        total_sum = questions.aggregate(Sum('score'))
        return total_sum['score__sum'] or 0

    user_score = serializers.SerializerMethodField(read_only=True)
    max_score = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_time', 'end_time', 'instructions',
                  'user_score', 'max_score', 'banner_image',]


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_time', 'end_time', 'banner_image']


class UserContestSerializer(serializers.ModelSerializer):
    contest_id = ContestListSerializer()
    user_contest_id = serializers.IntegerField(source='id')

    class Meta:
        model = UserContest
        fields = ['user_contest_id', 'contest_id', 'status', 'total_score',
                  'total_penalty']
        depth = 2


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = ['que_id', 'score', 'penalty']


class LeaderBoardSerializer(serializers.ModelSerializer):
    questions = UserQuestionSerializer(read_only=True, many=True)
    user_id = UserSafeInfoSerializer(read_only=True)

    class Meta:
        model = UserContest
        fields = ['user_id', 'total_score', 'total_penalty', 'questions']

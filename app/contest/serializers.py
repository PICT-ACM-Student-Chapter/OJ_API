from rest_framework import serializers

from contest.models import Contest
from core.models import UserContest
from question.serializers import QuestionListSerializer


class ContestSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_time', 'end_time', 'instructions',
                  'questions']


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_time', 'end_time']


class UserContestSerializer(serializers.ModelSerializer):
    contest_id = ContestListSerializer()

    class Meta:
        model = UserContest
        fields = ['id', 'contest_id', 'status', 'score']
        depth = 2

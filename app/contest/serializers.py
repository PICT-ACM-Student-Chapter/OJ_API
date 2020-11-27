from rest_framework import serializers

from contest.models import Contest, ContestQue
from core.models import UserContest


class ContestQueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestQue
        fields = ['order', 'question']
        depth = 2

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        que_repr = representation.pop('question')
        for key in que_repr:
            representation[key] = que_repr[key]
        return representation


class ContestSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, model):
        return ContestQueSerializer(
            ContestQue.objects.filter(contest_id=model.id), many=True).data

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
        fields = ['id', 'contest_id', 'status']
        depth = 2

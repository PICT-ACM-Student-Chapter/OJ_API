from rest_framework import serializers

from contest.models import Contest
from core.models import UserContest
from core.serializers import UserSafeInfoSerializer


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_time', 'end_time']


class ContestSerializer(serializers.ModelSerializer):
    user_id = UserSafeInfoSerializer()
    contest_id = ContestListSerializer()

    class Meta:
        model = UserContest
        fields = '__all__'
        depth = 2

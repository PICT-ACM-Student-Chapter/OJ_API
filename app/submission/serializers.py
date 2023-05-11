from dataclasses import field
from pyexpat import model
from rest_framework import serializers

from .models import RunSubmission, Submission, Verdict


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verdict
        fields = ['id', 'test_case', 'status']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
        }


class RunSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunSubmission
        fields = ['id', 'lang_id', 'status', 'code', 'stdin', 'stdout',
                  'stderr', 'exec_time', 'mem']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
            'stdout': {'required': False, 'read_only': True},
            'stderr': {'required': False, 'read_only': True},
            'exec_time': {'required': False, 'read_only': True},
            'mem': {'required': False, 'read_only': True},
            'code': {'write_only': True}
        }


class SubmissionSerializer(serializers.ModelSerializer):
    verdicts = serializers.SerializerMethodField()

    def get_verdicts(self, instance):
        verdicts = instance.verdicts.order_by('test_case_id')
        return VerdictSerializer(verdicts,
                                 many=True).data  # many=True is required

    class Meta:
        model = Submission
        fields = ['id', 'code', 'lang_id', 'score', 'ques_id', 'verdicts',
                  'contest']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'verdicts': {'required': False, 'read_only': True},
            'contest': {'required': False, 'read_only': True},
            'ques_id': {'required': False, 'read_only': True},
            'score': {'required': False, 'read_only': True},
            'code': {'write_only': True}
        }


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'code', 'lang_id', 'ques_id', 'status',
                  'score', 'created_at']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'code': {'required': False, 'read_only': True},
            'lang_id': {'required': False, 'read_only': True},
            'ques_id': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
            'score': {'required': False, 'read_only': True},
            'created_at': {'required': False, 'read_only': True},
        }


class RunRCSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunSubmission
        fields = ['id', 'status', 'stdin', 'stdout',
                  'stderr', 'exec_time', 'mem']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
            'stdin': {'required': True},
            'stdout': {'required': False, 'read_only': True},
            'stderr': {'required': False, 'read_only': True},
            'exec_time': {'required': False, 'read_only': True},
            'mem': {'required': False, 'read_only': True},
        }
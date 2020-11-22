from rest_framework import serializers

from .models import RunSubmission, Submission


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
        }


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'code', 'lang_id', 'ques_id']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
        }

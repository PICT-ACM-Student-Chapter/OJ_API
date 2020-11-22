from rest_framework import serializers

from .models import RunSubmission, Submission, Verdict


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verdict
        fields = ['test_case', 'status']
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
        }


class SubmissionSerializer(serializers.ModelSerializer):
    verdicts = VerdictSerializer(read_only=True,
                                 many=True)  # many=True is required

    class Meta:
        model = Submission
        fields = ['id', 'code', 'lang_id', 'ques_id', 'verdicts']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'verdicts': {'required': False, 'read_only': True},

        }


class SubmissionListSerializer(serializers.ModelSerializer):
    verdicts = VerdictSerializer(read_only=True,
                                 many=True)  # many=True is required

    class Meta:
        model = Submission
        fields = ['id', 'code', 'lang_id', 'ques_id', 'verdicts']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'verdicts': {'required': False, 'read_only': True},
            'code': {'required': False, 'read_only': True},
            'lang_id': {'required': False, 'read_only': True},
            'ques_id': {'required': False, 'read_only': True},
        }

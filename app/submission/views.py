# Create your views here.
import os

from django.forms import model_to_dict
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from submission.judge0_utils import submit_to_run
from submission.models import RunSubmission
from submission.permissions import IsRunInTime, IsRunSelf
from submission.serializers import RunSubmissionSerializer


class Run(CreateAPIView):
    serializer_class = RunSubmissionSerializer
    permission_classes = [IsRunInTime]

    def perform_create(self, serializer):
        judge0_token = submit_to_run(
            model_to_dict(serializer.validated_data['lang_id']),
            serializer.validated_data['code'],
            serializer.validated_data['stdin'],
            os.environ['JUDGE0_RUN_CALLBACK_URL'])
        serializer.save(user_id=self.request.user, judge0_token=judge0_token)


class CheckRunStatus(RetrieveAPIView):
    serializer_class = RunSubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = RunSubmission.objects.all()
    permission_classes = [IsRunInTime, IsRunSelf]

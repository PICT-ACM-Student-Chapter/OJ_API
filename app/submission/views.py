# Create your views here.
import os

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from submission.judge0_utils import submit_to_run
from submission.models import RunSubmission
from submission.permissions import IsRunInTime, IsRunSelf
from submission.serializers import RunSubmissionSerializer

STATUSES = {
    1: 'IN_QUEUE',
    2: 'PROCESSING',
    3: 'AC',
    4: 'WA',
    5: 'TLE',
    6: 'CE',
    7: 'SIGSEGV',
    8: 'SIGXFSZ',
    9: 'SIGFPE',
    10: 'SIGABRT',
    11: 'NZEC',
    12: 'RTE',
    13: 'IE',
    14: 'EFE'
}


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


class CallbackRunNow(APIView):
    serializer_class = RunSubmissionSerializer

    def put(self, request):
        run_submission = RunSubmission.objects.filter(
            judge0_token=request.data['token']).first()
        run_submission.stdout = request.data['stdout']
        run_submission.stderr = request.data['stderr'] or request.data[
            'message'] or request.data[
                                    'compile_output'] or ''
        run_submission.exec_time = request.data['time']
        run_submission.mem = request.data['memory']
        status = request.data['status']['id']
        run_submission.status = STATUSES[status]

        run_submission.save()

        return JsonResponse({})

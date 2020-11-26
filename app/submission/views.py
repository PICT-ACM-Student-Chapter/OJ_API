# Create your views here.
import os

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.views import APIView

from question.models import Question
from submission.models import RunSubmission, Verdict, Submission
from submission.permissions import IsRunInTime, IsRunSelf, IsSubmissionInTime
from .judge0_utils import submit_to_run, submit_to_submit
from .serializers import RunSubmissionSerializer, SubmissionSerializer, \
    SubmissionListSerializer

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
        serializer.save(user_id=self.request.user)
        submit_to_run(
            model_to_dict(serializer.validated_data['lang_id']),
            serializer.validated_data['code'],
            serializer.validated_data['stdin'],
            '{}/{}'.format(os.environ['JUDGE0_RUN_CALLBACK_URL'],
                           serializer.data['id']))


class CheckRunStatus(RetrieveAPIView):
    serializer_class = RunSubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = RunSubmission.objects.all()
    permission_classes = [IsRunInTime, IsRunSelf]


class Submit(CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsSubmissionInTime]

    def perform_create(self, serializer):
        sub = serializer.save(user_id=self.request.user)

        submit_to_submit(
            sub,
            model_to_dict(serializer.validated_data['lang_id']),
            serializer.validated_data['code'],
            serializer.validated_data['ques_id'],
            os.environ['JUDGE0_SUBMIT_CALLBACK_URL'])


class SubmissionList(ListAPIView):
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        try:
            ques_id = self.kwargs['ques_id']
            que = Question.objects.get(id=ques_id)
            return Submission.objects.filter(user_id=self.request.user,
                                             ques_id=que)
        except Question.DoesNotExist:
            raise exceptions.NotFound('No Submissions Found')


class SubmissionStatus(RetrieveAPIView):
    serializer_class = SubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = Submission.objects.all()
    permission_classes = [IsRunSelf]


class CallbackRunNow(APIView):

    def put(self, request, sub_id):
        print(request.data)
        run_submission = RunSubmission.objects.filter(
            id=sub_id).first()
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


class CallbackSubmission(APIView):

    def put(self, request, verdict_id):
        print(request.data)
        verdict_submission = Verdict.objects.filter(
            id=verdict_id).first()
        verdict_submission.stdout = request.data['stdout']
        verdict_submission.stderr = request.data['stderr'] or request.data[
            'message'] or request.data['compile_output'] or ''
        verdict_submission.exec_time = request.data['time']
        verdict_submission.mem = request.data['memory']
        status = request.data['status']['id']
        verdict_submission.status = STATUSES[status]

        verdict_submission.save()
        return JsonResponse({})

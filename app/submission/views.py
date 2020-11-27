# Create your views here.
import os

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.views import APIView

from app import settings
from contest.models import ContestQue, Contest
from core.models import UserQuestion, UserContest
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
        contest = Contest.objects.filter(id=self.kwargs['contest_id']).first()
        question = Question.objects.filter(id=self.kwargs['ques_id']).first()

        sub = serializer.save(user_id=self.request.user, contest=contest,
                              ques_id=question)

        submit_to_submit(
            sub,
            model_to_dict(serializer.validated_data['lang_id']),
            serializer.validated_data['code'],
            question,
            os.environ['JUDGE0_SUBMIT_CALLBACK_URL'])


# TODO: Query with contest_id
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
        # Save the verdict
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

        # Get submission object and all verdict object for the submission
        submission = verdict_submission.submission
        verdicts = Verdict.objects.filter(submission=submission)

        # Check if there are no verdicts in queue
        # (i.e. this is last verdict of the submission)
        if verdicts.filter(status='IN_QUEUE').count() == 0:
            # Update submission object
            if ContestQue.objects.filter(
                    question=submission.ques_id,
                    contest=submission.contest
            ).first().is_binary:
                # Binary
                if verdicts.exclude(status='AC').count() == 0:
                    # All ACs
                    submission.score = submission.ques_id.score
                    submission.status = 'AC'
                    submission.save()
                    self.update_user_question(submission)  # TODO: change name
                else:
                    # TODO: Write logic for internal err and CE
                    if verdict_submission.status == 'CE':
                        submission.status = 'CE'
                    else:
                        submission.status = 'WA'
                    submission.save()
            else:
                # Partial
                weight = 0
                total_weight = 0
                for v in verdicts:
                    total_weight += v.test_case.weightage
                    if v.status == 'AC':
                        weight += v.test_case.weightage
                score = (submission.ques_id.score * weight / total_weight)
                submission.score = round(score, 2)

                if (weight / total_weight) == 1:
                    submission.status = 'AC'
                elif verdict_submission.status == 'CE':
                    submission.status = 'CE'
                elif weight == 0:
                    submission.status = 'WA'
                else:
                    submission.status = 'PA'

                submission.save()
                self.update_user_question(submission)

        return JsonResponse({})

    def update_user_question(self, sub):

        user_ques = UserQuestion.objects.filter(
            que=sub.ques_id,
            user_contest__user_id=sub.user_id,
            user_contest__contest_id=sub.contest
        )

        if not user_ques.exists():
            # UserQue doesn't exists, so create one
            user_contest = UserContest.objects.filter(
                user_id=sub.user_id,
                contest_id=sub.contest
            ).first()

            user_que = UserQuestion.objects.create(
                que=sub.ques_id,
                user_contest=user_contest
            )
        else:
            # UserQue exists, so select the first
            user_que = user_ques.first()

        # If UserQue score is less than or equal to que score already,
        # no need to update (only best one with min time-penalty is considered)
        if sub.score <= user_que.score:
            return

        # Score improved, update UserQue
        user_que.score = sub.score

        # Time penalty
        time_penalty = (sub.created_at - sub.contest.start_time).seconds / 60
        time_penalty = round(time_penalty, 2)
        # WA penalty
        no_of_wa = Submission.objects.filter(
            status__in=['WA', 'PA'], ques_id=sub.ques_id,
            contest=sub.contest, user_id=sub.user_id
        ).count()
        wa_penalty = settings.PENALTY_MINUTES * no_of_wa

        # Total penalty
        user_que.penalty = (time_penalty + wa_penalty)
        user_que.save()

# Create your views here.
import os

from django.conf import settings
from django.core.cache import cache
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from contest.models import ContestQue, Contest
from core.models import UserQuestion, UserContest
from question.models import Question, Testcase
from submission.models import RunSubmission, Verdict, Submission
from submission.permissions import IsRunInTime, IsRunSelf, IsSubmissionInTime
from utils import b64_sub_str, b64_encode
from submission.throttles import RunThrottle, RunRCThrottle, SubmitThrottle
from .judge0_utils import submit_to_run, submit_to_submit, delete_submission
from .serializers import RunSubmissionSerializer, SubmissionSerializer, \
    SubmissionListSerializer, RunRCSerializer

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
    throttle_classes = [RunThrottle]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
        try:
            submit_to_run(
                model_to_dict(serializer.validated_data['lang_id']),
                serializer.validated_data['code'],
                serializer.validated_data['stdin'],
                '{}/{}'.format(os.environ['JUDGE0_RUN_CALLBACK_URL'],
                               serializer.data['id']))
        except KeyError:
            submit_to_run(
                model_to_dict(serializer.validated_data['lang_id']),
                serializer.validated_data['code'],
                '',
                '{}/{}'.format(os.environ['JUDGE0_RUN_CALLBACK_URL'],
                               serializer.data['id']))


class RunRC(CreateAPIView):
    serializer_class = RunRCSerializer
    permission_classes = [IsSubmissionInTime]
    throttle_classes = [RunRCThrottle]

    def perform_create(self, serializer):
        contest_que = ContestQue.objects.filter(
            contest__id=self.kwargs['contest_id'],
            question__id=self.kwargs['ques_id'],
            is_reverse_coding=True
        )

        fq = contest_que.first()

        if not fq:
            raise exceptions.NotFound('No Question Found')

        serializer.save(user_id=self.request.user, code='TkE=',
                        lang_id=fq.question.correct_code_lang)
        # 'NA' b64
        code = b64_encode(fq.question.correct_code)
        lang = fq.question.correct_code_lang

        submit_to_run(
            model_to_dict(lang),
            code,
            serializer.validated_data['stdin'],
            '{}/{}'.format(os.environ['JUDGE0_RUN_CALLBACK_URL'],
                           serializer.data['id']))


class CheckRunStatus(RetrieveAPIView):
    serializer_class = RunSubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = RunSubmission.objects.all()
    permission_classes = [IsRunInTime, IsRunSelf]

    def get(self, request, *args, **kwargs):
        res = cache.get('run_{}'.format(self.kwargs['id']))
        if not res:
            res = self.retrieve(request, *args, **kwargs).data
            cache.set('run_{}'.format(self.kwargs['id']), res,
                      settings.CACHE_TTLS['RUN'])
        return Response(data=res)


class Submit(CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsSubmissionInTime]
    throttle_classes = [SubmitThrottle]

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


class SubmissionList(ListAPIView):
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        ques_id = self.kwargs['ques_id']
        contest_id = self.kwargs['contest_id']
        # cache_key = "subs_list_u{}_c{}_q{}".format(self.request.user.id,
        #                                            ques_id, contest_id)
        # subs_list = cache.get(cache_key)
        subs_list = []
        try:
            que = Question.objects.get(id=ques_id)
            subs_list = Submission.objects.filter(
                user_id=self.request.user,
                ques_id=que,
                contest_id=contest_id) \
                .order_by('-created_at')
        except Question.DoesNotExist:
            raise exceptions.NotFound('No Submissions Found')
        return subs_list


class SubmissionStatus(RetrieveAPIView):
    serializer_class = SubmissionSerializer
    lookup_url_kwarg = 'id'
    queryset = Submission.objects.all()
    permission_classes = [IsRunSelf]

    def get(self, request, *args, **kwargs):
        cache_key = 'submit_{}'.format(self.kwargs['id'])
        res = cache.get(cache_key)
        if not res:
            res = self.retrieve(request, *args, **kwargs).data
            cache.set(cache_key, res, settings.CACHE_TTLS['SUBMISSION'])
        else:
            self.check_permissions(request)
        return Response(data=res)


class CallbackRunNow(APIView):

    def put(self, request, sub_id):
        stdout = request.data['stdout']
        stderr = request.data['stderr'] or request.data[
            'message'] or request.data['compile_output'] or ''
        stdout = b64_sub_str(stdout or '', settings.MAX_RUN_OUTPUT_LENGTH)
        stderr = b64_sub_str(stderr or '', settings.MAX_RUN_OUTPUT_LENGTH)

        status = request.data['status']['id']

        RunSubmission.objects.filter(
            id=sub_id).update(
            stdout=stdout,
            stderr=stderr,
            exec_time=request.data['time'],
            mem=request.data['memory'],
            status=STATUSES[status]
        )

        cache.delete('run_{}'.format(sub_id))
        delete_submission(request.data['token'])

        return JsonResponse({})


class CallbackSubmission(APIView):

    def put(self, request, verdict_id):
        # Save the verdict
        print(request.data['status']['description'])
        status = request.data['status']['id']
        # Query1 (defined and called)
        Verdict.objects.filter(id=verdict_id).update(
            exec_time=request.data['time'],
            mem=request.data['memory'],
            status=STATUSES[status],
        )

        request._mutable = True
        request = {}
        # delete_submission(request.data['token'])

        # update single verdict from cache
        submission = Verdict.objects.get(id=verdict_id).submission
        cache_key = 'submit_{}'.format(submission.id)
        c = cache.get(cache_key)
        if c:
            # if present then only update it
            # iterate through verdicts and update the status
            for i in range(len(c['verdicts'])):
                if c['verdicts'][i]['id'] == verdict_id:
                    c['verdicts'][i]['status'] = STATUSES[status]
                    break
            cache.set(cache_key, c, settings.CACHE_TTLS['SUBMISSION'])

        # verdict_submission.stdout = (request.data['stdout'])[:100]
        # verdict_submission.stderr = (request.data['stderr'] or request.data[
        #     'message'] or request.data['compile_output'] or '')[:100]

        # Get submission object and all verdict object for the submission
        # Query2 (defined)
        verdicts = Verdict.objects.filter(submission__verdicts__id=verdict_id)

        # Check if there are no verdicts in queue
        # (i.e. this is last verdict of the submission)

        in_queue_count = 0
        ac_count = 0
        # Query2 (called)
        for v in verdicts:
            if v.status == 'IN_QUEUE':
                in_queue_count += 1
            elif v.status == 'AC':
                ac_count += 1

        if in_queue_count == 0:
            cache.delete(cache_key)
            # Query4
            if ContestQue.objects.filter(
                    question_id=submission.ques_id_id,
                    contest_id=submission.contest_id
            ).first().is_binary:
                # Binary
                if ac_count == len(verdicts):
                    # All ACs
                    submission.score = submission.ques_id.score
                    submission.status = 'AC'
                    # Query5
                    submission.save()
                    self.update_user_question(submission)
                else:
                    # Priority: RTE > TLE > WA > AC
                    submission.status = 'IE'
                    for v in verdicts:
                        if v.status == 'CE':
                            submission.status = 'CE'
                            break
                        # Check for all types of RTE
                        if v.status in ['SIGSEGV', 'SIGXFSZ', 'SIGFPE',
                                        'SIGABRT', 'NZEC', 'RTE']:
                            submission.status = 'RTE'
                            break
                        if v.status == 'TLE':
                            submission.status = 'TLE'
                            break
                        if v.status == 'WA':
                            submission.status = 'WA'
                            break

                    # Query5
                    submission.save()
                    self.update_user_question(submission)
            else:
                # Partial
                weight = 0
                total_weight = 0

                # Query5
                test_cases = Testcase.objects.filter(verdict__in=verdicts)

                for v in verdicts:
                    for tc in test_cases:
                        if tc.id == v.test_case_id:
                            v.test_case = tc
                            break
                    total_weight += v.test_case.weightage
                    if v.status == 'AC':
                        weight += v.test_case.weightage
                # Query6 (for question)
                score = (submission.ques_id.score * weight / total_weight)
                submission.score = round(score, 2)

                if (weight / total_weight) == 1:
                    submission.status = 'AC'
                elif status == 'CE':
                    submission.status = 'CE'
                elif weight == 0:
                    submission.status = 'WA'
                else:
                    submission.status = 'PA'

                # Query7
                submission.save()
                self.update_user_question(submission)

        data = {
            "status": "success"
        }
        print(data)
        return Response(data={}, status=200)

    @staticmethod
    def update_user_question(sub):
        # Time penalty
        time_penalty = (sub.created_at - sub.contest.start_time).seconds / 60
        time_penalty = round(time_penalty, 2)
        # WA penalty
        # Query2
        no_of_wa = Submission.objects.filter(
            status__in=['WA', 'PA'], ques_id=sub.ques_id,
            contest=sub.contest, user_id=sub.user_id
        ).count()
        wa_penalty = settings.PENALTY_MINUTES * no_of_wa
        try:
            user_que = UserQuestion.objects.get(
                que_id=sub.ques_id_id,
                user_contest__user_id_id=sub.user_id_id,
                user_contest__contest_id_id=sub.contest_id
            )

            # Query1 If UserQue score is less than or equal to que score
            # already, no need to update (only best one with min
            # time-penalty is considered)

            # WHEN SUBMITTED FIRST WA PENALTY WAS NOT ADDDED,
            # SO WHEN 2 PEOPLE WILL HAVE WAs FOR A QUESTION THEN PENALTIES
            # SHOULD PE CONSIDERED
            if sub.score <= (user_que.score if user_que else 0):
                return

            # Score improved, update UserQue

            # Total penalty
            #  Query3
            user_que.score = sub.score
            user_que.penalty = round(time_penalty + wa_penalty, 2)
            user_que.save()
        except UserQuestion.DoesNotExist:
            user_contest = UserContest.objects.get(
                user_id_id=sub.user_id_id,
                contest_id_id=sub.contest_id,
            )
            UserQuestion.objects.create(
                que_id=sub.ques_id_id,
                user_contest=user_contest,
                score=sub.score,
                penalty=round(time_penalty + wa_penalty, 2)
                if sub.score > 0 else 0
            )

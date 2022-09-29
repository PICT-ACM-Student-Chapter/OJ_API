# Create your models here.
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User
from django.db import models

from contest.models import Contest
from core.models import Language
from question.models import Question, Testcase

IN_QUEUE = 'IN_QUEUE'
PROCESSING = 'PROCESSING'
STATUSES = [
    ('IN_QUEUE', 'In Queue'),
    ('PROCESSING', 'Processing'),
    ('AC', 'Accepted'),
    ('WA', 'Wrong Answer'),
    ('TLE', 'Time Limit Exceeded'),
    ('CE', 'Compilation Error'),
    ('SIGSEGV', 'Runtime Error (SIGSEGV)'),
    ('SIGXFSZ', 'Runtime Error (SIGXFSZ)'),
    ('SIGFPE', 'Runtime Error (SIGFPE)'),
    ('SIGABRT', 'Runtime Error (SIGABRT)'),
    ('RTE', 'Runtime Error (other)'),
    ('NZEC', 'Runtime Error (NZEC)'),
    ('IE', 'Internal Error'),
    ('EFE', 'Exec Format Error'),
]
PENDING = 'PENDING'
FINAL_STATUSES = [
    ('IN_QUEUE', 'In Queue'),
    ('AC', 'Accepted'),
    ('PA', 'Partially Accepted'),
    ('CE', 'Compilation Error'),
    ('IE', 'Internal Error'),
    ('WA', 'Anything else'),
]

HACK_STATUSES = [
    ('PENDING', 'pending'),
    ('SUCCESS', 'Hack Successful'),
    ('FAILURE', 'Hack Unsuccessful'),
]


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    status = models.CharField(max_length=32, choices=FINAL_STATUSES,
                              default=IN_QUEUE)


class Verdict(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=32, choices=STATUSES,
                              default=IN_QUEUE)
    test_case = models.ForeignKey(Testcase, on_delete=models.CASCADE)
    submission = models.ForeignKey(to=Submission, related_name='verdicts',
                                   on_delete=models.CASCADE)
    stdout = models.TextField(null=True, blank=True)
    stderr = models.TextField(null=True, blank=True)
    exec_time = models.CharField(max_length=10, null=True)
    mem = models.CharField(max_length=10, null=True)


class RunSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUSES,
                              default=IN_QUEUE)
    stdin = models.TextField(blank=True)
    stdout = models.TextField(null=True, blank=True)
    stderr = models.TextField(null=True, blank=True)
    exec_time = models.CharField(max_length=10, null=True)
    mem = models.CharField(max_length=10, null=True)


class HackSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    correct_code_submission_id = models.ForeignKey(
        to=RunSubmission, on_delete=models.CASCADE, related_name='correct_code_submission')
    incorrect_code_submission_id = models.ForeignKey(
        to=RunSubmission, on_delete=models.CASCADE, related_name='incorrect_code_submission')
    status = models.CharField(
        max_length=32, choices=HACK_STATUSES, default=PENDING)

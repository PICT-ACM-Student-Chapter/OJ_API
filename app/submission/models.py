# Create your models here.
from core.models import Language
from django.contrib.auth.models import User
from django.db import models
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


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)


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
    judge0_token = models.CharField(max_length=40)


class RunSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    judge0_token = models.CharField(max_length=40)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUSES,
                              default=IN_QUEUE)
    stdin = models.TextField(blank=True)
    stdout = models.TextField(null=True, blank=True)
    stderr = models.TextField(null=True, blank=True)
    exec_time = models.CharField(max_length=10, null=True)
    mem = models.CharField(max_length=10, null=True)

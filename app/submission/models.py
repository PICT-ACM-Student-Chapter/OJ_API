# Create your models here.
from core.models import Language
from django.contrib.auth.models import User
from django.db import models
from question.models import Question, Testcase


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)


class Verdict(models.Model):
    IN_QUEUE = 'IN_QUEUE'
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
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
        ('NZEC', 'Runtime Error (NZEC)'),
        ('IE', 'Internal Error'),
        ('EFE', 'Exec Format Error'),
    ]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=32, choices=STATUSES)
    test_case = models.ForeignKey(Testcase, on_delete=models.CASCADE)
    submission = models.ForeignKey(to=Submission, related_name='verdicts',
                                   on_delete=models.CASCADE)

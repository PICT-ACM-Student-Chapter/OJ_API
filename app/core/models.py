from contest.models import Contest
from django.contrib.auth.models import User
from django.db import models


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    stack_limit = models.IntegerField()
    mem_limit = models.IntegerField()
    filesize_limit = models.IntegerField()
    process_limit = models.IntegerField()
    time_limit = models.IntegerField()


class UserContest(models.Model):
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    score = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['contest_id', 'user_id', ]),
        ]

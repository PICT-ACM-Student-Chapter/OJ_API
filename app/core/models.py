from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from contest.models import Contest


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    judge0_lang_id = models.CharField(max_length=3)
    monaco_lang_code = models.CharField(max_length=20, default='cpp')
    stack_limit = models.IntegerField(default=2048)
    cpu_time_limit = models.IntegerField(default=2)
    # mem_limit should be >= 2048 as expected by judge0
    mem_limit = models.IntegerField(validators=[MinValueValidator(2048)],
                                    default=2048)
    filesize_limit = models.IntegerField(default=1024)
    process_limit = models.IntegerField(default=50)
    wall_time_limit = models.IntegerField(default=3)

    def __str__(self):
        return "{} - ID{}".format(self.name, self.id)


class UserContest(models.Model):
    STATUSES = [
        ('REGISTERED', 'REGISTERED'),
        ('STARTED', 'STARTED'),
        ('ENDED', 'ENDED')
    ]
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE,
                                   related_name='user_contests')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUSES,
                              default='REGISTERED')

    @property
    def total_score(self):
        user_ques = UserQuestion.objects.filter(user_contest=self)
        total_sum = user_ques.aggregate(Sum('score'))
        return total_sum['score__sum'] or 0.0

    @property
    def total_penalty(self):
        user_ques = UserQuestion.objects.filter(user_contest=self)
        total_sum = user_ques.aggregate(Sum('penalty'))
        return total_sum['penalty__sum'] or 0.0

    class Meta:
        indexes = [
            models.Index(fields=['contest_id', 'user_id', ]),
        ]

    def __str__(self):
        return "{}-{}".format(self.contest_id.name, self.user_id.username)


class UserQuestion(models.Model):
    que = models.ForeignKey(to='question.Question', on_delete=models.CASCADE,
                            null=True)

    user_contest = models.ForeignKey(UserContest, on_delete=models.CASCADE,
                                     related_name='questions')
    penalty = models.FloatField(default=0)
    score = models.FloatField(default=0)

    class Meta:
        unique_together = ['user_contest', 'que']

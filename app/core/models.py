from contest.models import Contest
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

User._meta.get_field('email')._unique = True


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    judge0_lang_id = models.CharField(max_length=3)
    stack_limit = models.IntegerField()
    cpu_limit = models.IntegerField()
    # mem_limit should be >= 2048 as expected by judge0
    mem_limit = models.IntegerField(validators=[MinValueValidator(2048)])
    filesize_limit = models.IntegerField()
    process_limit = models.IntegerField()
    time_limit = models.IntegerField()

    def __str__(self):
        return "{} - ID{}".format(self.name, self.id)


class UserContest(models.Model):
    STATUSES = [
        ('REGISTERED', 'REGISTERED'),
        ('STARTED', 'STARTED'),
        ('ENDED', 'ENDED')
    ]
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUSES)
    score = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['contest_id', 'user_id', ]),
        ]

    def __str__(self):
        return "{}-{}".format(self.contest_id.name, self.user_id.username)

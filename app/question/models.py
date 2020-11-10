from contest.models import Contest
from django.db import models


# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    contest_id = models.ForeignKey(Contest, on_delete=models.SET_NULL,
                                   null=True)
    score = models.IntegerField()


class Testcase(models.Model):
    id = models.IntegerField(primary_key=True)
    input = models.FileField()

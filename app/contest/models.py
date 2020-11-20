from django.db import models

# Create your models here.
from question.models import Question


class Contest(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    instructions = models.TextField()
    questions = models.ManyToManyField(to=Question, related_name='contests',
                                       through='ContestQue')


class ContestQue(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ['contest', 'order']

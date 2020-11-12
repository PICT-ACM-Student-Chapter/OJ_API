# Create your models here.
from core.models import Language
from django.contrib.auth.models import User
from django.db import models
from question.models import Question


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.TextField()
    verdict = models.CharField(max_length=20)

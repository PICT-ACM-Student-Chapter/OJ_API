import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def upload_input_rename(instance, filename):
    que_id = instance.que_id.id
    print(instance)
    return "question_{}/testcases/input{}.txt". \
        format(que_id, uuid.uuid4().hex)


def upload_output_rename(instance, filename):
    que_id = instance.que_id.id
    return "question_{}/testcases/output{}.txt". \
        format(que_id, uuid.uuid4().hex)


# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    score = models.IntegerField()
    input_format = models.TextField(default="")
    output_format = models.TextField(default="")
    constraints = models.TextField(default="")
    correct_code = models.TextField(blank=True, null=True)
    correct_code_lang = models.ForeignKey(to='core.Language', null=True,
                                          on_delete=models.SET_NULL)

    def __str__(self):
        return "{} - ID{}".format(self.name, self.id)


class Testcase(models.Model):
    id = models.AutoField(primary_key=True)
    input = models.FileField(upload_to=upload_input_rename)
    output = models.FileField(upload_to=upload_output_rename)
    que_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                               related_name="test_cases")
    is_public = models.BooleanField(default=False)
    weightage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=1)

    def __str__(self):
        return "{} - TC{}".format(self.que_id.name, self.id)

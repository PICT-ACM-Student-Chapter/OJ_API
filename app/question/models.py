from django.db import models


def upload_input_rename(instance, filename):
    que_id = instance.que_id.id
    return "question_{}/testcases/input{}.txt". \
        format(que_id, instance.id)


def upload_output_rename(instance, filename):
    que_id = instance.que_id.id
    return "question_{}/testcases/output{}.txt". \
        format(que_id, instance.id)


# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    score = models.IntegerField()


class Testcase(models.Model):
    id = models.IntegerField(primary_key=True)
    input = models.FileField(upload_to=upload_input_rename)
    output = models.FileField(upload_to=upload_output_rename)
    que_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                               related_name="test_cases")
    is_public = models.BooleanField(default=False)

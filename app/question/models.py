from django.db import models

from contest.models import Contest


def upload_file_rename(field_name):
    allowed_field_names = ['input', 'output']
    if not field_name or field_name not in allowed_field_names:
        raise Exception("field_name should be either of " +
                        str(allowed_field_names))

    def wrapper(instance, filename):
        que_id = instance.que_id.id
        contest_id = instance.que_id.contest_id.id
        return "contest_{}/question_{}/testcases/{}{}.txt". \
            format(contest_id, que_id, field_name, instance.id)

    return wrapper


# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    contest_id = models.ForeignKey(Contest, on_delete=models.SET_NULL,
                                   null=True, related_name="questions")
    score = models.IntegerField()


class Testcase(models.Model):
    id = models.IntegerField(primary_key=True)
    input = models.FileField(upload_to=upload_file_rename("input"))
    output = models.FileField(upload_to=upload_file_rename("output"))
    que_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                               related_name="test_cases")
    is_public = models.BooleanField(default=False)

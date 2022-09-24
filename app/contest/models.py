from django.db import models

# Create your models here.
from question.models import Question


def upload_contest_banner(instance, filename):
    return "contest-banners/banner-{}.{}". \
        format(instance.id, filename.split('.')[-1])


class Contest(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ems_slot_id = models.CharField(max_length=30)
    banner_image = models.FileField(upload_to=upload_contest_banner, null=True, blank=True)
    instructions = models.TextField()
    questions = models.ManyToManyField(to=Question, related_name='contests',
                                       through='ContestQue')

    def __str__(self):
        return "{} (ID{})".format(self.name, self.id)

    class Meta:
        indexes = [
            models.Index(fields=['ems_slot_id']),
        ]


class ContestQue(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_binary = models.BooleanField(default=False)
    is_reverse_coding = models.BooleanField(default=False)
    is_hacking = models.BooleanField(default=False)
    order = models.IntegerField()

    class Meta:
        unique_together = ['contest', 'order']

from django.db import models
from martor.models import MartorField


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = MartorField()

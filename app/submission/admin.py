from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from submission.models import Submission


# Register your models here.

class SubmissionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


# Register your models here.
admin.site.register(Submission, SubmissionModelAdmin)

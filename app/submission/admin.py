from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from submission.models import Submission, Verdict, RunSubmission


# Register your models here.

class VerdictInline(admin.TabularInline):
    model = Verdict


class SubmissionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [
        VerdictInline,
    ]


class RunSubmissionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


# Register your models here.
admin.site.register(Submission, SubmissionModelAdmin)
admin.site.register(RunSubmission, RunSubmissionModelAdmin)
admin.site.register(Verdict)

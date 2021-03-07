import base64

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from martor.widgets import AdminMartorWidget

from submission.models import Submission, Verdict, RunSubmission


# Register your models here.

class VerdictInline(admin.TabularInline):
    model = Verdict


class SubmissionModelAdmin(admin.ModelAdmin):
    fields = ['user_id', 'ques_id', 'lang_id', 'score', 'status', 'contest',
              'user_code', 'code']
    list_display = ('user_id', 'ques_id', 'contest', 'score', 'status')
    list_filter = ('user_id', 'ques_id', 'contest')
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [
        VerdictInline,
    ]
    readonly_fields = ["user_code", ]

    def user_code(self, obj):
        base64_bytes = obj.code.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return format_html('<pre>{}</pre>', sample_string)


class RunSubmissionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


# Register your models here.
admin.site.register(Submission, SubmissionModelAdmin)
admin.site.register(RunSubmission, RunSubmissionModelAdmin)
admin.site.register(Verdict)

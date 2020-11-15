from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from question.models import Question, Testcase


# Register your models here.

class QuestionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


# Register your models here.
admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Testcase)

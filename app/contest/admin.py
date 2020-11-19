from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from contest.models import Contest


# Register your models here.
from question.models import Question


class QuestionsInline(admin.TabularInline):
    model = Question.contests.through
    verbose_name = "Question"
    verbose_name_plural = "Contest Questions"


class ContestModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [QuestionsInline]
    exclude = ['questions']


admin.site.register(Contest, ContestModelAdmin)

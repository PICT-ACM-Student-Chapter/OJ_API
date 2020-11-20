from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from contest.models import Contest, ContestQue


# Register your models here.


class QuestionsInline(admin.TabularInline):
    model = ContestQue
    verbose_name = "Question"
    verbose_name_plural = "Contest Questions"


class ContestModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [QuestionsInline]
    exclude = ['questions']


admin.site.register(Contest, ContestModelAdmin)

from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from question.models import Question, Testcase


# Register your models here.

class TestCasesInline(admin.TabularInline):
    model = Testcase
    verbose_name = "Testcase"
    verbose_name_plural = "Testcases"


class QuestionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [TestCasesInline]
    list_display = ('name', 'score')
    search_fields = ('name', 'score')


class TestcaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'que_id', 'is_public')
    list_filter = ('que_id', 'is_public')


# Register your models here.
admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Testcase, TestcaseAdmin)

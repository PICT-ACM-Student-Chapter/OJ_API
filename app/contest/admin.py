from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from martor.widgets import AdminMartorWidget

from contest.models import Contest, ContestQue
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from core.models import UserContest


class QuestionsInline(admin.TabularInline):
    model = ContestQue
    verbose_name = "Question"
    verbose_name_plural = "Contest Questions"


class ContestUsersInline(admin.TabularInline):
    model = UserContest
    verbose_name = "User"
    verbose_name_plural = "Registered Users"
    readonly_fields = ('status', )


class UserContestInline(admin.TabularInline):
    model = UserContest
    verbose_name = "Contest"
    verbose_name_plural = "Registered Contests"
    readonly_fields = ('status', )


class ContestModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = [QuestionsInline, ContestUsersInline]
    exclude = ['questions']
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)


class MyUserAdmin(UserAdmin):
    inlines = [UserContestInline]


admin.site.register(Contest, ContestModelAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

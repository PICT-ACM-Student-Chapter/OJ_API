from contest.models import Contest
from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget


# Register your models here.

class ContestModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(Contest, ContestModelAdmin)

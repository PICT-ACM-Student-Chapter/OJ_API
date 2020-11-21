# Register your models here.
from django.contrib import admin

from core.models import Language, UserContest

admin.site.site_header = 'PASC OJ Management Portal'
admin.site.site_title = 'PASC OJ Management Portal'


class UserContestAdmin(admin.ModelAdmin):
    list_display = ('contest_id', 'user_id', 'status', 'score')
    list_filter = ('contest_id', 'user_id', 'status')
    search_fields = ('contest_id', 'user_id')


admin.site.register(Language)
admin.site.register(UserContest, UserContestAdmin)

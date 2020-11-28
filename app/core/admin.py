# Register your models here.
from core.models import Language, UserContest, UserQuestion
from django.contrib import admin

admin.site.site_header = 'PASC OJ Management Portal'
admin.site.site_title = 'PASC OJ Management Portal'


class UserQuestionInline(admin.TabularInline):
    model = UserQuestion


class UserContestAdmin(admin.ModelAdmin):
    list_display = (
        'contest_id', 'user_id', 'status', 'total_score', 'total_penalty')
    list_filter = ('contest_id', 'user_id', 'status')
    search_fields = ('contest_id', 'user_id')
    inlines = [
        UserQuestionInline,
    ]


admin.site.register(Language)
admin.site.register(UserContest, UserContestAdmin)
admin.site.register(UserQuestion)

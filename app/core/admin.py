# Register your models here.
from core.models import Language, UserContest
from django.contrib import admin


admin.site.site_header = 'PASC OJ Management Portal'
admin.site.site_title = 'PASC OJ Management Portal'

admin.site.register(Language)
admin.site.register(UserContest)

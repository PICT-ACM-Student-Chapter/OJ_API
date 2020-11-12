from django.conf.urls import url

from contest.views import Contests

urlpatterns = [
    url(r'^/$', Contests.as_view()),
]

"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="PASC Online Judge API",
        default_version='v1',
        description="API for PASC Online Judge backend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pict.acm@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=os.environ.get('BASE_URL', 'https://api.onlinejudge.ml')
)

urlpatterns = [
                  url(r'^swagger(?P<format>\.json|\.yaml)$',
                      schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
                  url(r'^swagger/$', schema_view.with_ui('swagger',
                                                         cache_timeout=0),
                      name='schema-swagger-ui'),
                  url(r'^redoc/$', schema_view.with_ui('redoc',
                                                       cache_timeout=0),
                      name='schema-redoc'),
                  url(r'^jet/', include('jet.urls', 'jet')),
                  url(r'^auth/', include('djoser.urls')),
                  url(r'^auth/', include('djoser.urls.jwt')),
                  path('admin/', admin.site.urls),
                  path('martor/', include('martor.urls')),
                  path('contests/', include('contest.urls')),
                  path('', include('core.urls')),
                  path('questions/', include('question.urls')),
                  path('', include('submission.urls')),

              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

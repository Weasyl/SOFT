from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fb.views.index'),
    url(r'^ajax/vouch/$', 'fb.views.vouch'),
    url(r'^ajax/correct/$', 'fb.views.correct'),
    
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

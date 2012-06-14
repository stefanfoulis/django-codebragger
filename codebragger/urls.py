#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from .views import ProjectDetailView, ProjectListView
from .validation import VARIABLE_AND_DASH_ALLOWED_CHARS

urlpatterns = patterns('',
    url(r'^$', ProjectListView.as_view(), name='codebragger_project_list'),
    url(r'^(?P<slug>[\.' + VARIABLE_AND_DASH_ALLOWED_CHARS + r']+)/$', ProjectDetailView.as_view(), name='codebragger_project_detail'),
)

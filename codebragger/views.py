#-*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Project


class ProjectListView(ListView):
    model = Project

class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        kwargs.update({
            'projects': Project.objects.all(),
            'project': kwargs.get('object'),
        })
        return kwargs
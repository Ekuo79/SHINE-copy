from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from companies.models import Companies

class ApplyView(TemplateView):
    template_name = 'apply/apply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Companies.objects.all()
        return context
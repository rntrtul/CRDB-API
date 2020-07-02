from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import logging

from .models import Campaign
# Create your views here.

class IndexView(generic.ListView):
  template_name = 'campaigns/index.html'
  context_object_name = 'campaign_list'

  def get_queryset(self):
    return Campaign.objects.order_by('num')

class DetailView(generic.DetailView):
  model = Campaign
  template_name = 'campaigns/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['ep_list'] = context['object'].episodes.order_by('num')
    return context

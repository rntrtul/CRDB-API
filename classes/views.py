from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Class

class IndexView(generic.ListView):
  template_name = 'classes/index.html'
  context_object_name = 'class_list'

  def get_queryset(self):
    return Class.objects.order_by('name')
    #filter(first_name__in=[item['first_name'] for item in distinct])


class DetailView(generic.DetailView):
  model = Class
  template_name = 'classes/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['char_list'] = context['object'].sheets.distinct('stat_sheet__character_id')
    return context

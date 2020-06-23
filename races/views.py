from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Race

class IndexView(generic.ListView):
  template_name = 'races/index.html'
  context_object_name = 'race_list'

  def get_queryset(self):
    return Race.objects.order_by('name')

class DetailView(generic.DetailView):
  model = Race
  template_name = 'races/detail.html'

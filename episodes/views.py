from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Episode
# Create your views here.

class IndexView(generic.ListView):
  template_name = 'episodes/index.html'
  context_object_name = 'ep_list'

  def get_queryset(self):
    return Episode.objects.order_by('title')

class DetailView(generic.DetailView):
  model = Episode
  template_name = 'episodes/detail.html'

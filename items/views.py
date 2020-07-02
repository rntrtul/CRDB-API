from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Potion, PotionUsage

class IndexView(generic.ListView):
  template_name = 'items/index.html'
  context_object_name = 'item_list'

  def get_queryset(self):
    #return Character.objects.order_by('first_name')
    return Potion.objects.all()

class DetailView(generic.DetailView):
  model = Potion
  template_name = 'items/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['usage_list'] = context['object'].uses.order_by('episode_id')
    return context

class PotionUsageDetailView(generic.DetailView):
  model = PotionUsage
  template_name = 'items/potionUsageDetail.html'



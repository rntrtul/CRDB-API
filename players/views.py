from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from .models import Player
class IndexView(generic.ListView):
  template_name = 'players/index.html'
  context_object_name = 'player_list'

  def get_queryset(self):
    return Player.objects.order_by('full_name')

class DetailView(generic.DetailView):
  model = Player
  template_name = 'players/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['char_list'] = context['object'].characters.order_by('full_name')
    return context
  
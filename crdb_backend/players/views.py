from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from rest_framework import generics, viewsets
from .serializers import PlayerSerializer
from .models import Player

# REST views
class PlayerViewSet(viewsets.ModelViewSet):
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

# django template views
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
    context['attendance_list'] = context['object'].attendance.order_by('episode__campaign', 'episode__num')
    context['attendance_count'] = context['attendance_list'].count()
    return context
  

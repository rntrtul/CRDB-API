from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from rest_framework import generics, viewsets
from .serializers import SpellSerializer,SpellDetailSerializer, SpellCastSerializer, LearnedSpellSerializer
from .models import Spell, SpellCast, LearnedSpell

# REST views
class SpellViewSet(viewsets.ModelViewSet):
  def get_serializer_class(self):
    if self.action == 'list':
      return SpellSerializer
    elif self.action == 'retrieve':
      return SpellDetailSerializer

  def get_queryset(self):
    if self.action == 'list':
      queryset = Spell.objects.all().order_by('name')
      queryset = self.get_serializer_class().setup_eager_loading(queryset)
    elif self.action == 'retrieve':
      queryset = Spell.objects.all()
    return queryset
  

class SpellCastViewSet(viewsets.ModelViewSet):
  queryset = SpellCast.objects.all()
  serializer_class = SpellCastSerializer

class LearnedSpellViewSet(viewsets.ModelViewSet):
  queryset = LearnedSpell.objects.all()
  serializer_class = LearnedSpellSerializer

# django template views
class IndexView(generic.ListView):
  template_name = 'spells/index.html'
  context_object_name = 'spell_list'

  def get_queryset(self):
    #return Character.objects.order_by('first_name')
    return Spell.objects.all()

class DetailView(generic.DetailView):
  model = Spell
  template_name = 'spells/detail.html'
  
  #def get_object(self): 
  #  name= self.kwargs.get("name")       
  #  return get_object_or_404(Spell, name=name)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cast_list'] = context['object'].casts.order_by('episode_id')
    return context

class CastDetailView(generic.DetailView):
  model = SpellCast
  template_name = 'spells/castDetail.html'

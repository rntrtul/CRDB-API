from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from rest_framework import generics
from .serializers import SpellSerializer, SpellCastSerializer, LearnedSpellSerializer
from .models import Spell, SpellCast, LearnedSpell

# REST views
class SpellList(generics.ListAPIView):
  queryset = Spell.objects.all()
  serializer_class = SpellSerializer

class SpellDetail(generics.RetrieveAPIView):
  queryset = Spell.objects.all()
  serializer_class = SpellSerializer

class SpellCastList(generics.ListAPIView):
  queryset = SpellCast.objects.all()
  serializer_class = SpellCastSerializer

class SpellCastDetail(generics.RetrieveAPIView):
  queryset = SpellCast.objects.all()
  serializer_class = SpellCastSerializer

class LearnedSpellList(generics.ListAPIView):
  queryset = LearnedSpell.objects.all()
  serializer_class = LearnedSpellSerializer

class LearnedSpellDetail(generics.RetrieveAPIView):
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

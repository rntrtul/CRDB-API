from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from .models import CombatEncounter, CombatApperance, InitiativeOrder
from rolls.models import Rolls
from .serializers import CombatEncounterSerializer, CombatApperanceSerializer, InitiativeOrderSerializer
from rest_framework import generics
# Create your views here.

# REST views
class CombatEncounterList(generics.ListAPIView):
  queryset = CombatEncounter.objects.all()
  serializer_class = CombatEncounterSerializer

class CombatEncounterDetail(generics.RetrieveAPIView):
  queryset = CombatEncounter.objects.all()
  serializer_class = CombatEncounterSerializer

class CombatApperanceList(generics.ListAPIView):
  queryset = CombatApperance.objects.all()
  serializer_class = CombatApperanceSerializer

class CombatApperanceDetail(generics.RetrieveAPIView):
  queryset = CombatApperance.objects.all()
  serializer_class = CombatApperanceSerializer

class InitiativeOrderList(generics.ListAPIView):
  queryset = InitiativeOrder.objects.all()
  serializer_class = InitiativeOrderSerializer

class InitiativeOrderDetail(generics.RetrieveAPIView):
  queryset = InitiativeOrder.objects.all()
  serializer_class = InitiativeOrderSerializer

# Django template views
class IndexView(generic.ListView):
  template_name = 'encounters/index.html'
  context_object_name = 'encounters_list'
  paginate_by = 100

  def get_queryset(self):
    return CombatEncounter.objects.all()

class DetailView(generic.DetailView):
  model = CombatEncounter
  template_name = 'encounters/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['apperances'] = context['object'].apperances.order_by('character__name')
    context['initiative_order'] = context['object'].initiatievs.order_by('rank')
    encounter = context['object']
    context['rolls_list'] = Rolls.objects.filter(ep=encounter.episode,time_stamp__range=(encounter.start,encounter.end)).order_by('time_stamp')
    return context
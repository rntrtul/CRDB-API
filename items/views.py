from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
from .models import Potion, PotionUsage, Weapon, WeaponDamage, WeaponUsage, WeaponOwned
from rest_framework import generics,  viewsets
from .serializers import PotionSerializer, PotionDetailSerializer, PotionUsageSerializer, WeaponSerializer, WeaponDetailSerializer, WeaponDamageSerializer, WeaponOwnedSerializer, WeaponUsageSerializer

# REST views
class PotionViewSet(viewsets.ModelViewSet):
  def get_serializer_class(self):
    if self.action == 'list':
      return PotionSerializer
    elif self.action == 'retrieve':
      return PotionDetailSerializer

  queryset = Potion.objects.all().order_by('name')

class PotionUsageViewSet(viewsets.ModelViewSet):
  queryset = PotionUsage.objects.all()
  serializer_class = PotionUsageSerializer

class WeaponViewSet(viewsets.ModelViewSet):
  def get_serializer_class(self):
    if self.action == 'list':
      return WeaponSerializer
    elif self.action == 'retrieve':
      return WeaponDetailSerializer
      
  queryset = Weapon.objects.all().order_by('name')


class WeaponDamageViewSet(viewsets.ModelViewSet):
  queryset = WeaponDamage.objects.all()
  serializer_class = WeaponDamageSerializer

class WeaponUsageViewSet(viewsets.ModelViewSet):
  queryset = WeaponUsage.objects.all()
  serializer_class = WeaponUsageSerializer

class WeaponOwnedViewSet(viewsets.ModelViewSet):
  queryset = WeaponOwned.objects.all()
  serializer_class = WeaponOwnedSerializer

#django tempalte views
class IndexView(generic.ListView):
  template_name = 'items/index.html'
  context_object_name = 'item_list'

  def get_queryset(self):
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

class WeaponIndexView(generic.ListView):
  template_name = 'items/weaponIndex.html'
  context_object_name = 'weapon_list'
  
  def get_queryset(self):
    return Weapon.objects.order_by('name')

class WeaponDetailView(generic.DetailView):
  model = Weapon
  template_name = 'items/weaponDetail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['damages'] = context['object'].damages.all()
    context['owners'] = context['object'].owners.distinct('sheet__character__name')
    context['uses'] = context['object'].uses.all()
    context['total_dealt'] = context['uses'].aggregate(Sum('roll__final_value'))
    return context
from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Sum

from .models import Potion, PotionUsage, Weapon, WeaponDamage

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
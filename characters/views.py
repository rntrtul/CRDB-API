from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
import logging
from .models import Character, CharacterType, StatSheet

logger = logging.getLogger(__name__)
class IndexView(generic.ListView):
  template_name = 'characters/index.html'
  context_object_name = 'character_list'

  def get_queryset(self):
    return Character.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')
    #return Character.objects.order_by('first_name')

class DetailView(generic.DetailView):
  model = Character
  template_name = 'characters/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['display_rolls'] = context['object'].rolls.all()[:100]
    context['total_rolls'] = context['object'].rolls.count()
    context['statsheets'] = context['object'].stat_sheets.order_by('max_health')
    return context
class TypeListView(generic.ListView):
  template_name = 'characters/typeIndex.html'
  context_object_name = 'type_list'

  def get_queryset(self):
    return CharacterType.objects.order_by('name')

class TypeDetailView(generic.DetailView):
  model = CharacterType
  template_name = 'characters/typeDetail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['char_list'] = context['object'].characters.order_by('full_name')
    return context

class StatDetailView(generic.DetailView):
  model = StatSheet
  template_name = 'characters/stat-sheetDetail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['ability_scores'] = reversed(context['object'].ability_scores.all())
    context['saving_throws'] = reversed(context['object'].saving_throws.all())
    context['skills'] = context['object'].skills.order_by('skill__name')
    context['spells'] = context['object'].learned_spells.all()
    return context


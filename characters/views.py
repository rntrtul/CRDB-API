from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count, Sum
import logging
from .models import Ability, AbilityScore, Alignment, Character, CharacterType, ClassTaken, SavingThrow, Skill, SkillList, StatSheet
from rolls.models import RollType
from rest_framework import generics
from .serializers import (AbilitySerializer, AbilityScoreSerializer, AlignmentSerializer, CharacterSerializer, CharacterTypeSerializer, ClassTakenSerializer,
                          SavingThrowSerializer, SkillSerializer, SkillListSerializer, StatSheetSerializer)

# REST views
class AbilityList(generics.ListAPIView):
  queryset = Ability.objects.all()
  serializer_class = AbilitySerializer

class AbilityDetail(generics.RetrieveAPIView):
  queryset = Ability.objects.all()
  serializer_class = AbilitySerializer

class AbilityScoreList(generics.ListAPIView):
  queryset = AbilityScore.objects.all()
  serializer_class = AbilityScoreSerializer

class AbilityScoreDetail(generics.RetrieveAPIView):
  queryset = AbilityScore.objects.all()
  serializer_class = AbilityScoreSerializer

class AlignmentList(generics.ListAPIView):
  queryset = Alignment.objects.all()
  serializer_class = AlignmentSerializer

class AlignmentDetail(generics.RetrieveAPIView):
  queryset = Alignment.objects.all()
  serializer_class = AlignmentSerializer

class CharacterList(generics.ListAPIView):
  queryset = Character.objects.all()
  serializer_class = CharacterSerializer

class CharacterDetail(generics.RetrieveAPIView):
  queryset = Character.objects.all()
  serializer_class = CharacterSerializer

class CharacterTypeList(generics.ListAPIView):
  queryset = CharacterType.objects.all()
  serializer_class = CharacterTypeSerializer

class CharacterTypeDetail(generics.RetrieveAPIView):
  queryset = CharacterType.objects.all()
  serializer_class = CharacterTypeSerializer

class ClassTakenList(generics.ListAPIView):
  queryset = ClassTaken.objects.all()
  serializer_class = ClassTakenSerializer

class ClassTakenDetail(generics.RetrieveAPIView):
  queryset = ClassTaken.objects.all()
  serializer_class = ClassTakenSerializer

class SavingThrowList(generics.ListAPIView):
  queryset = SavingThrow.objects.all()
  serializer_class = SavingThrowSerializer

class SavingThrowDetail(generics.RetrieveAPIView):
  queryset = SavingThrow.objects.all()
  serializer_class = SavingThrowSerializer

class SkillsList(generics.ListAPIView):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class SkillsDetail(generics.RetrieveAPIView):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class SkillListList(generics.ListAPIView):
  queryset = SkillList.objects.all()
  serializer_class = SkillListSerializer

class SkillListDetail(generics.RetrieveAPIView):
  queryset = SkillList.objects.all()
  serializer_class = SkillListSerializer

class StatSheetList(generics.ListAPIView):
  queryset = StatSheet.objects.all()
  serializer_class = StatSheetSerializer

class StatSheetDetail(generics.RetrieveAPIView):
  queryset = StatSheet.objects.all()
  serializer_class = StatSheetSerializer


# Django template views
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
    damage_rolls = context['object'].rolls.filter(roll_type=RollType.objects.get(name="Damage"))
    if damage_rolls.count() != 0:
      context['damage_dealt'] = damage_rolls.aggregate(Sum('final_value'))
      context['avg_damage_dealt'] = round(context['damage_dealt']['final_value__sum'] / damage_rolls.count(), 2)
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
    context['level_up'] = context['object'].level_ups.all()
    context['langs'] = context['object'].languages.all()
    context['weapons'] = context['object'].weapons_owned.all()
    return context


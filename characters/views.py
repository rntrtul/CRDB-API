from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Character, CharacterType

class IndexView(generic.ListView):
  template_name = 'characters/index.html'
  context_object_name = 'character_list'

  def get_queryset(self):
    return Character.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')
    #return Character.objects.order_by('first_name')

class DetailView(generic.DetailView):
  model = Character
  template_name = 'characters/detail.html'

class TypeListView(generic.ListView):
  template_name = 'characters/typeIndex.html'
  context_object_name = 'type_list'

  def get_queryset(self):
    return CharacterType.objects.order_by('name')

class TypeDetailView(generic.DetailView):
  model = CharacterType
  template_name = 'characters/typeDetail.html'


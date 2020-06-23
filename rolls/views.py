from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Rolls, RollType
# Create your views here.

class IndexView(generic.ListView):
  template_name = 'rolls/index.html'
  context_object_name = 'rolls_list'

  def get_queryset(self):
    return Rolls.objects.order_by('time_stamp')

class DetailView(generic.DetailView):
  model = Rolls
  template_name = 'rolls/detail.html'

class TypeListView(generic.ListView):
  template_name = 'rolls/typeIndex.html'
  context_object_name = 'type_list'

  def get_queryset(self):
    return RollType.objects.order_by('name')

class TypeDetailView(generic.DetailView):
  model = RollType
  template_name = 'rolls/typeDetail.html'
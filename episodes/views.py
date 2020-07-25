from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Episode, Apperance, LevelProg
from rolls.models import Rolls
# Create your views here.
class IndexView(generic.ListView):
  template_name = 'episodes/index.html'
  context_object_name = 'ep_list'

  def get_queryset(self):
    #return Episode.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')
    return Episode.objects.order_by('campaign','num')

class DetailView(generic.DetailView):
  model = Episode
  template_name = 'episodes/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['apperances'] = context['object'].apperances.order_by('character__name')
    context['rolls'] = context['object'].rolls.order_by('time_stamp')
    context['level_progs'] = context['object'].level_ups.order_by('sheet__character__full_name')
    context['encounters'] = context['object'].combat_encounters.order_by('start')
    links = context['object'].vod_links
    context['yt_link'] = "https://youtu.be/" + links.all()[0].link_key + "?t="
    return context

class ApperanceIndexView(generic.ListView):
  template_name = 'episodes/apperanceIndex.html'
  context_object_name = 'apperance_list'
  paginate_by = 100

  def get_queryset(self):
    return Apperance.objects.order_by('episode')

class ApperanceDetailView(generic.DetailView):
  model = Apperance
  template_name = 'episodes/apperanceDetail.html'
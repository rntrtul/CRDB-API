from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Episode, Apperance
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
    context['apperances'] = context['object'].apperances.order_by('episode__num')
    context['rolls'] = context['object'].rolls.order_by('time_stamp')
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
from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count


from .models import Rolls, RollType
# Create your views here.

class IndexView(generic.ListView):
  template_name = 'rolls/index.html'
  context_object_name = 'rolls_list'
  paginate_by = 100

  def get_queryset(self):
    return Rolls.objects.order_by('ep','time_stamp')#only get first 100 otherwise too many

class DetailView(generic.DetailView):
  model = Rolls
  template_name = 'rolls/detail.html'

class TypeListView(generic.ListView):
  template_name = 'rolls/typeIndex.html'
  context_object_name = 'type_list'

  def get_queryset(self):
    return RollType.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')
    #return RollType.objects.order_by('name')

class TypeDetailView(generic.DetailView):
  model = RollType
  template_name = 'rolls/typeDetail.html'
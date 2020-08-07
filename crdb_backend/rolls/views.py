from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die
from .serializers import RollsSerializer, RollTypeSerializer,RollTypeDetailSerializer, AdvantageSerializer, AdvantageTypeSerializer, KillSerializer, DieSerializer
from rest_framework import generics, viewsets

# Create your views here.
#REST views
class RollsViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    queryset = Rolls.objects.all()[:5000]
    queryset = self.get_serializer_class().setup_eager_loading(queryset)
    return queryset

  serializer_class = RollsSerializer

class RollTypeViewSet(viewsets.ModelViewSet):

  def get_serializer_class (self):
    if self.action =='list':
      return RollTypeSerializer
    else: return RollTypeDetailSerializer

  queryset = RollType.objects.all()

class AdvantageTypeViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    if self.action == 'list':
        return  AdvantageType.objects.order_by('name')
    return AdvantageType.objects.all()

  serializer_class = AdvantageTypeSerializer

class AdvantageViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    if self.action == 'list':
        return  Advantage.objects.order_by('used__ep')
    return Advantage.objects.all()

  serializer_class = AdvantageSerializer

class KillViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    if self.action == 'list':
        return  Kill.objects.order_by('-count', 'roll')
    return Kill.objects.all()

  serializer_class = KillSerializer

class DieViewSet(viewsets.ModelViewSet):
  queryset = Die.objects.order_by('sides')
  serializer_class = DieSerializer

#django template views
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

class TypeDetailView(generic.DetailView):
  model = RollType
  template_name = 'rolls/typeDetail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['roll_list'] = context['object'].rolls.order_by('ep__num', 'time_stamp')[:100]
    context['c1_count'] = context['object'].rolls.filter(ep__campaign_id=5).count()
    context['c2_count'] = context['object'].rolls.filter(ep__campaign_id=6).count()
    return context
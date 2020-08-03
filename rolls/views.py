from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die
from .serializers import RollsSerializer, RollTypeSerializer, AdvantageSerializer, AdvantageTypeSerializer, KillSerializer, DieSerializer
from rest_framework import generics

# Create your views here.
#REST views
class RollsList(generics.ListAPIView):
  queryset = Rolls.objects.order_by('ep','time_stamp')[:100]
  serializer_class = RollsSerializer

class RollsDetail(generics.RetrieveAPIView):
  queryset = Rolls.objects.all()
  serializer_class = RollsSerializer

class RollTypeList(generics.ListAPIView):
  queryset = RollType.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')
  serializer_class = RollTypeSerializer

class RollTypeDetail(generics.RetrieveAPIView):
  queryset = RollType.objects.all()
  serializer_class = RollTypeSerializer

class AdvantageTypeList(generics.ListAPIView):
  queryset = AdvantageType.objects.order_by('name')
  serializer_class = AdvantageTypeSerializer

class AdvantageTypeDetail(generics.RetrieveAPIView):
  queryset = AdvantageType.objects.all()
  serializer_class = AdvantageTypeSerializer

class AdvantageList(generics.ListAPIView):
  queryset = Advantage.objects.order_by('used__ep')
  serializer_class = AdvantageSerializer

class AdvantageDetail(generics.RetrieveAPIView):
  queryset = Advantage.objects.all()
  serializer_class = AdvantageSerializer

class KillList(generics.ListAPIView):
  queryset = Kill.objects.order_by('-count', 'roll')
  serializer_class = KillSerializer

class KillDetail(generics.RetrieveAPIView):
  queryset = Kill.objects.all()
  serializer_class = KillSerializer

class DieList(generics.ListAPIView):
  queryset = Die.objects.order_by('sides')
  serializer_class = DieSerializer

class DieDetail(generics.RetrieveAPIView):
  queryset = Die.objects.all()
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
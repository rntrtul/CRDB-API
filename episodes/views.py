from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from itertools import chain
from rest_framework import generics, viewsets
from .serializers import (EpisodeSerializer,EpisodeDetailSerializer, ApperanceSerializer, AttendanceSerializer, ApperanceTypeSerializer,
                          AttendanceTypeSerializer, LiveSerializer, VodLinksSerializer, VodTypeSerializer)
from .models import Episode, Apperance, LevelProg, VodType, Attendance, ApperanceType, AttendanceType, Live, VodLinks
from rolls.models import Rolls
# Create your views here.

#REST API views
class EpisodeViewSet(viewsets.ModelViewSet):
  def get_serializer_class(self):
    if self.action == 'list':
      return EpisodeSerializer
    elif self.action == 'retrieve':
      return EpisodeDetailSerializer

  def get_queryset(self):
    queryset = Episode.objects.order_by('campaign','num')
    if self.action == 'retrieve':
      queryset = self.get_serializer_class().setup_eager_loading(queryset)
    else:
      queryset = self.get_serializer_class().setup_eager_loading(queryset)

    return queryset

class ApperanceViewSet(viewsets.ModelViewSet):
  queryset = Apperance.objects.all()
  serializer_class = ApperanceSerializer

class ApperanceTypeViewSet(viewsets.ModelViewSet):
  queryset = ApperanceType.objects.order_by('name')
  serializer_class = ApperanceTypeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
  queryset = Attendance.objects.all()
  serializer_class = AttendanceSerializer

class AttendanceTypeViewSet(viewsets.ModelViewSet):
  queryset = AttendanceType.objects.order_by('name')
  serializer_class = AttendanceTypeSerializer

class LiveViewSet(viewsets.ModelViewSet):
  queryset = Live.objects.order_by('episode')
  serializer_class = LiveSerializer

class VodTypeViewSet(viewsets.ModelViewSet):
  queryset = VodType.objects.order_by('name')
  serializer_class = VodTypeSerializer

class VodLinksViewSet(viewsets.ModelViewSet):
  queryset = VodLinks.objects.all()
  serializer_class = VodLinksSerializer


# django template views 
class IndexView(generic.ListView):
  template_name = 'episodes/index.html'
  context_object_name = 'ep_list'

  def get_queryset(self):
    return Episode.objects.order_by('campaign','num')

class DetailView(generic.DetailView):
  model = Episode
  template_name = 'episodes/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['apperances'] = context['object'].apperances.order_by('character__name')
    context['level_progs'] = context['object'].level_ups.order_by('sheet__character__full_name')
    context['encounters'] = context['object'].combat_encounters.order_by('start')
    yt_links = context['object'].vod_links.filter(vod_type=VodType.objects.get(name="YouTube")).all()
    
    if context['object'].campaign.num == 1 and (context['object'].num == 31 or context['object'].num == 33 or context['object'].num == 35):
      context['yt_link'] = "https://youtu.be/" + yt_links[0].link_key + "?t="
      context['yt_link_p2'] = "https://youtu.be/" + yt_links[1].link_key + "?t="
      context['rolls'] = chain(context['object'].rolls.filter(notes__startswith='p1').order_by('time_stamp'),context['object'].rolls.filter(notes__startswith='p2').order_by('time_stamp'))
    else:
      context['rolls'] = context['object'].rolls.order_by('time_stamp')
      context['yt_link'] = "https://youtu.be/" + yt_links[0].link_key + "?t="
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
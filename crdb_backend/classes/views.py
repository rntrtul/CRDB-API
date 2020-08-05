from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from rest_framework import generics, viewsets
from .serializers import ClassSerializer
from .models import Class

#REST views
class ClassViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    if self.action == 'list':
        return Class.objects.order_by('name')
    return Class.objects.all()

  serializer_class = ClassSerializer

class ClassDetail(generics.RetrieveAPIView):
  queryset = Class.objects.all()
  serializer_class = ClassSerializer


# Django Template Views
class IndexView(generic.ListView):
  template_name = 'classes/index.html'
  context_object_name = 'class_list'

  def get_queryset(self):
    return Class.objects.order_by('name')

class DetailView(generic.DetailView):
  model = Class
  template_name = 'classes/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['char_list'] = context['object'].sheets.distinct('stat_sheet__character_id')
    return context

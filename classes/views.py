from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Class

class IndexView(generic.ListView):
  template_name = 'classes/index.html'
  context_object_name = 'class_list'

  def get_queryset(self):
    return Class.objects.order_by('name')

class DetailView(generic.DetailView):
  model = Class
  template_name = 'classes/detail.html'

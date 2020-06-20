from django.shortcuts import get_object_or_404,  render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Rolls
# Create your views here.

class IndexView(generic.ListView):
  template_name = 'rolls/index.html'
  context_object_name = 'rolls_list'

  def get_queryset(self):
    return Rolls.objects.order_by('-time')[:5]

class DetailView(generic.DetailView):
  model = Rolls
  template_name = 'rolls/detail.html'

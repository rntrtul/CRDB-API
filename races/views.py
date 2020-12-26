from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from rest_framework import generics, viewsets
from .serializers import RaceSerializer
from .models import Race


# REST views
class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class IndexView(generic.ListView):
    template_name = 'races/index.html'
    context_object_name = 'race_list'

    def get_queryset(self):
        return Race.objects.order_by('name')


class DetailView(generic.DetailView):
    model = Race
    template_name = 'races/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['char_list'] = context['object'].characters.order_by('full_name')
        return context

from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import DamageSerializer, DamageTypeSerializer
from .models import Damage, DamageType

# Create your views here.
class DamageViewSet(viewsets.ModelViewSet):
  def get_queryset(self):
    if self.action == 'list':
        return  Damage.objects.order_by('-points').all()[:500]
    return Damage.objects.all()

  serializer_class = DamageSerializer

  
class DamageTypeViewSet(viewsets.ModelViewSet):
  queryset = DamageType.objects.order_by('name')
  serializer_class = DamageTypeSerializer


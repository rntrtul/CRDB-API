from django.shortcuts import render
from rest_framework import generics
from .serializers import DamageSerializer, DamageTypeSerializer
from .models import Damage, DamageType

# Create your views here.
class DamageList(generics.ListAPIView):
  queryset = Damage.objects.order_by('-points').all()[:500]
  serializer_class = DamageSerializer

class DamageDetail(generics.RetrieveAPIView):
  queryset = Damage.objects.all()
  serializer_class = DamageSerializer
  
class DamageTypeList(generics.ListAPIView):
  queryset = DamageType.objects.order_by('name')
  serializer_class = DamageTypeSerializer

class DamageTypeDetail(generics.RetrieveAPIView):
  queryset = DamageType.objects.order_by('name')
  serializer_class = DamageTypeSerializer


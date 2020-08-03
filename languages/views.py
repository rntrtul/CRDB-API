from django.shortcuts import render
from rest_framework import generics
from .serializers import LanguageSerializer, LearnedLanguageSerializer
from .models import Language, LearnedLanguage
# Create your views here.

# REST views
class LanguageList(generics.ListAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer

class LanguageDetail(generics.RetrieveAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer

class LearnedLanguageList(generics.ListAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer

class LearnedLanguageDetail(generics.RetrieveAPIView):
  queryset = LearnedLanguage.objects.all()
  serializer_class = LearnedLanguageSerializer
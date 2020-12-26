from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import LanguageSerializer, LearnedLanguageSerializer
from .models import Language, LearnedLanguage


# Create your views here.

# REST views
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LearnedLanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

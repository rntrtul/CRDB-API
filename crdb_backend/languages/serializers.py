from rest_framework import serializers
from .models import Language, LearnedLanguage

class LanguageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Language
    fields = ('id', 'name')

class LearnedLanguageSerializer(serializers.ModelSerializer):
  class Meta:
      model = LearnedLanguage
      fields = ('id', 'language', 'sheet')



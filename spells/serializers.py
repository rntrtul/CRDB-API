from rest_framework import serializers
from .models import Spell, SpellCast, LearnedSpell

class SpellSerializer(serializers.ModelSerializer):
  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'cantrip')

class SpellCastSerializer(serializers.ModelSerializer):
  class Meta:
    model = SpellCast
    fields = ('id', 'timestamp', 'spell', 'character', 'cast_level', 'notes', 'episode')

class LearnedSpellSerializer(serializers.ModelSerializer):
  class Meta:
    model = LearnedSpell
    fields = ('id', 'spell', 'sheet')

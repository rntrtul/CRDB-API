from rest_framework import serializers
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die

class RollsSerializer(serializers.ModelSerializer):
  class Meta:
      model = Rolls
      fields = ('id', 'time_stamp', 'natural_value', 'final_value', 'notes', 'damage', 'roll_type', 'ep', 'character', 'kill_count')

class RollTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = RollType
    fields = ('id', 'name')

class AdvantageTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = AdvantageType
    fields = ('id', 'name')

class AdvantageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Advantage
    fields = ('id', 'type', 'used', 'disregarded')

class KillSerializer(serializers.ModelSerializer):
  class Meta:
    model = Kill
    fields = ('id', 'roll','killed', 'count')

class DieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Die
    fields = ('id', 'sides')
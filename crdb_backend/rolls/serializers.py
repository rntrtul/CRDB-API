from rest_framework import serializers
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die

class RollsSerializer(serializers.ModelSerializer):
  class Meta:
      model = Rolls
      fields = ('id', 'ep', 'time_stamp','character', 'roll_type','natural_value', 'final_value', 'notes', 'damage', 'kill_count')

  def __init__(self, *args, **kwargs):
    fields = kwargs.pop('fields', None)

    super(RollsSerializer, self).__init__(*args, **kwargs)

    if fields is not None:
      allowed = set(fields)
      existing = set(self.fields)
      for field_name in existing - allowed:
          self.fields.pop(field_name)

class RollTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = RollType
    fields = ('id', 'name')

class RollTypeDetailSerializer(serializers.ModelSerializer):
  count = serializers.SerializerMethodField()

  class Meta:
    model = RollType
    fields = ('id', 'name', 'count', 'rolls')
  
  def get_count(self, instance):
    return instance.rolls.count()

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
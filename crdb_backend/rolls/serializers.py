from rest_framework import serializers
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die

class RollsListSerializer (serializers.ListSerializer):

  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('character', 'roll_type', 'ep')
    return queryset
  
  class Meta:
      model = Rolls
      fields = '__all__'
      depth = 1

class RollsSerializer(serializers.ModelSerializer):
  ep = serializers.SerializerMethodField()
  character = serializers.SerializerMethodField()
  class Meta:
    list_serializer_class = RollsListSerializer
    model = Rolls
    fields = ('id', 'ep', 'time_stamp','character', 'roll_type','natural_value', 'final_value', 'notes', 'damage', 'kill_count')
    depth = 1
  
  def get_ep(self, instance):
    ep = instance.ep
    ep_info = {
      'id': ep.id,
      'title': ep.title,
      'num': ep.num,
      'campaign_num': ep.campaign.num,
      'vod_links': [{'link_key': ep.vod_links.all()[0].link_key}],
    }
    #vod link index is reversed since not sorted (so most recent ie. part 2 is index 0)
    if ep_info['campaign_num'] == 1 and (ep_info['num'] == 31 or ep_info['num'] == 33 or ep_info['num'] == 35):
      ep_info['vod_links'] = [{'link_key': ep.vod_links.all()[1].link_key}, 
                              {'link_key': ep.vod_links.all()[0].link_key}]
    return ep_info

  def get_character(self, instance):
    char = instance.character
    char_info = {
      'id': char.id,
      'name': char.name,
    }
    return char_info
  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('character', 'roll_type', 'ep', 'ep__campaign', 'ep__vod_links')
    return queryset

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
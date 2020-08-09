from rest_framework import serializers
from .models import Spell, SpellCast, LearnedSpell
from django.db.models import Count

class SpellSerializer(serializers.ModelSerializer):
  cast_count = serializers.SerializerMethodField()
  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'cantrip', 'cast_count')
  def get_cast_count(self,instance):
    return instance.casts.count()

  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('casts')
    return queryset

class SpellCastSerializer(serializers.ModelSerializer):
  episode = serializers.SerializerMethodField()
  class Meta:
    model = SpellCast
    fields = ('id', 'timestamp', 'spell', 'character', 'cast_level', 'notes', 'episode')
    depth = 1

  def get_episode(self, instance):
    ep = instance.episode
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

  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('character', 'spell', 'episode', 'skills')
    return queryset

class LearnedSpellSerializer(serializers.ModelSerializer):
  class Meta:
    model = LearnedSpell
    fields = ('id', 'spell')
    depth = 1

class SpellDetailSerializer(serializers.ModelSerializer):
  casts = serializers.SerializerMethodField()
  top_users = serializers.SerializerMethodField()

  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'cantrip', 'casts', 'top_users')
  
  def get_casts(self, instance):
    queryset = instance.casts.prefetch_related("character", "episode").prefetch_related("episode__campaign", "episode__vod_links")
    queryset = queryset.order_by('episode__campaign', 'episode__num')
    return SpellCastSerializer(queryset, many=True).data

  def get_top_users(self, instance):
    return instance.casts.values_list('character__name').annotate(character_uses=Count('character')).order_by('-character_uses')[:10]
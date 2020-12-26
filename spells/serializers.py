from rest_framework import serializers
from .models import Spell, SpellCast, LearnedSpell
from django.db.models import Count


class SpellSerializer(serializers.ModelSerializer):
    cast_count = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ('id', 'name', 'level', 'cantrip', 'cast_count')

    @staticmethod
    def get_cast_count(instance):
        return instance.casts.count()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(SpellSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('casts')
        return queryset


class SpellCastSerializer(serializers.ModelSerializer):
    episode = serializers.SerializerMethodField()
    character = serializers.SerializerMethodField()

    class Meta:
        model = SpellCast
        fields = ('id', 'timestamp', 'spell', 'character', 'cast_level', 'notes', 'episode')
        depth = 1

    @staticmethod
    def get_character(instance):
        char = instance.character
        return {
            'id': char.id,
            'name': char.name,
        }

    @staticmethod
    def get_episode(instance):
        ep = instance.episode
        ep_info = {
            'id': ep.id,
            'title': ep.title,
            'num': ep.num,
            'campaign_num': ep.campaign.num,
            'vod_links': [{'link_key': ep.vod_links.all()[0].link_key}],
        }
        # vod link index is reversed since not sorted (so most recent ie. part 2 is index 0)
        if ep_info['campaign_num'] == 1 and (ep_info['num'] == 31 or ep_info['num'] == 33 or ep_info['num'] == 35):
            ep_info['vod_links'] = [{'link_key': ep.vod_links.all()[1].link_key},
                                    {'link_key': ep.vod_links.all()[0].link_key}]
        return ep_info

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('character', 'spell', 'episode', 'episode__campaign', 'episode__vod_links')
        return queryset


class SpellCastInEpSerializer(serializers.ModelSerializer):
    character = serializers.SerializerMethodField()
    spell = SpellSerializer('spell', fields=('id', 'name'))

    class Meta:
        model = SpellCast
        fields = ('timestamp', 'spell', 'character', 'cast_level', 'notes')

    @staticmethod
    def get_character(instance):
        char = instance.character
        return {
            'id': char.id,
            'name': char.name,
        }


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

    @staticmethod
    def get_casts(instance):
        queryset = instance.casts.prefetch_related("character", "episode").prefetch_related("episode__campaign",
                                                                                            "episode__vod_links")
        queryset = queryset.order_by('episode__campaign', 'episode__num')
        return SpellCastSerializer(queryset, many=True).data

    @staticmethod
    def get_top_users(instance):
        return instance.casts.values_list('character__name').annotate(character_uses=Count('character')).order_by(
            '-character_uses')[:10]

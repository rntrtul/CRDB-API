from rest_framework import serializers
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die


class RollTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RollType
        fields = ('id', 'name')


class RollsSerializer(serializers.ModelSerializer):
    episode = serializers.SerializerMethodField()
    character = serializers.SerializerMethodField()
    roll_type = RollTypeSerializer('roll_type')

    class Meta:
        model = Rolls
        fields = (
          'id', 'episode', 'timestamp', 'character', 'roll_type', 'natural_value', 'final_value', 'notes', 'damage',
          'kill_count')

    @staticmethod
    def get_episode(instance):
        ep = instance.ep
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
    def get_character(instance):
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


class RollTypeDetailSerializer(serializers.ModelSerializer):
    rolls = serializers.SerializerMethodField()

    class Meta:
        model = RollType
        fields = ('id', 'name', 'rolls')
        depth = 2

    @staticmethod
    def get_rolls(instance):
        queryset = instance.rolls.order_by('ep__campaign', 'ep__num', 'timestamp')
        queryset = RollsSerializer.setup_eager_loading(queryset)

        return RollsSerializer(queryset, many=True, read_only=True).data


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
        fields = ('id', 'roll', 'killed', 'count')


class DieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Die
        fields = ('id', 'sides')

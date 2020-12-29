from rest_framework import serializers
from django.db.models import Sum, Count, Case, When, IntegerField
from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die
from episodes.models import Episode
from spells.models import SpellCast
from characters.models import Character


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


class RankingSerializer(serializers.ModelSerializer):
    episode_count = serializers.SerializerMethodField()
    game_time = serializers.SerializerMethodField()
    hdywt = serializers.SerializerMethodField()
    kills = serializers.SerializerMethodField()
    nat_twenty = serializers.SerializerMethodField()
    nat_one = serializers.SerializerMethodField()
    rolls_by_ep = serializers.SerializerMethodField()
    roll_count = serializers.SerializerMethodField()
    roll_type = serializers.SerializerMethodField()
    spells_by_ep = serializers.SerializerMethodField()

    class Meta:
        model = Rolls
        fields = ('episode_count', 'game_time', 'hdywt', 'kills', 'nat_one', 'nat_twenty', 'rolls_by_ep', 'roll_count',
                  'roll_type', 'spells_by_ep')

    @staticmethod
    def get_episode_count(instance):
        return Episode.objects.all().count()

    @staticmethod
    def get_game_time(instance):
        return Episode.objects.all().aggregate(Sum('length'))['length__sum']

    @staticmethod
    def get_hdywt(instance):
        return Rolls.objects.all().values_list('character__name').annotate(hdywt_count=Sum(
            Case(
                When(notes__contains="HDYWTDT", then=1),
                output_field=IntegerField()
            ))).order_by('-hdywt_count')

    @staticmethod
    def get_kills(instance):
        return Rolls.objects.all().values_list('character__name').annotate(kills_count=Count('kills')).order_by(
            '-kills_count')

    @staticmethod
    def get_nat_one(instance):
        return Rolls.objects.all().exclude(roll_type__name="Damage").values_list('character__name').annotate(
            nat_ones=Sum(
                Case(
                    When(natural_value=1, then=1),
                    output_field=IntegerField()
                ))).order_by('-nat_ones')

    @staticmethod
    def get_nat_twenty(instance):
        return Rolls.objects.all().exclude(roll_type__name="Damage").values_list('character__name').annotate(
            nat_twenty=Sum(
                Case(
                    When(natural_value=20, then=1),
                    output_field=IntegerField()
                ))).order_by('-nat_twenty')

    @staticmethod
    def get_rolls_by_ep(instance):
        campaign_one = Rolls.objects.all().filter(ep__campaign__num=1).values_list('ep__num').annotate(
            roll_count=Count('notes')).order_by('ep__num')
        campaign_two = Rolls.objects.all().filter(ep__campaign__num=2).values_list('ep__num').annotate(
            roll_count=Count('notes')).order_by('ep__num')
        return {"campaign_one": campaign_one, "campaign_two": campaign_two}

    @staticmethod
    def get_roll_count(instance):
        return Rolls.objects.all().count()

    @staticmethod
    def get_roll_type(instance):
        return [1, 2]

    @staticmethod
    def get_spells_by_ep(instance):
        campaign_one = SpellCast.objects.all().filter(episode__campaign__num=1).values_list('episode__num').annotate(
            spell_count=Count('notes')).order_by('episode__num')
        campaign_two = SpellCast.objects.all().filter(episode__campaign__num=2).values_list('episode__num').annotate(
            spell_count=Count('notes')).order_by('episode__num')
        return {"campaign_one": campaign_one, "campaign_two": campaign_two}

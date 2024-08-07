from rest_framework import serializers
from .models import Episode, ApperanceType, Apperance, Attendance, AttendanceType, Live, LevelProg, VodLinks, VodType
from rolls.serializers import RollsSerializer, RollTypeSerializer
from spells.serializers import SpellCastSerializer, SpellCastInEpSerializer
from encounters.serializers import CombatEncounterSerializer
from itertools import chain


class EpisodeSerializer(serializers.ModelSerializer):
    is_live = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ('id', 'campaign', 'num', 'title', 'length', 'is_live')
        depth = 1

    @staticmethod
    def get_is_live(instance):
        return instance.live_episodes.exists()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('campaign').prefetch_related('live_episodes')
        return queryset

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(EpisodeSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ApperanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApperanceType
        fields = ('id', 'name')


class ApperanceSerializer(serializers.ModelSerializer):
    # ep_title = serializers.SerializerMethodField()

    class Meta:
        model = Apperance
        fields = ('id', 'episode', 'apperance_type', 'character')
        depth = 1

    @staticmethod
    def get_ep_title(instance):
        return instance.episode.title

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('apperance_type')
        return queryset

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(ApperanceSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'episode', 'attendance_type', 'player')
        depth = 1

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('attendance_type')
        return queryset

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(AttendanceSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = ('id', 'episode', 'venue')


class AttendanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceType
        fields = ('id', 'name')


class LevelProgSerializer(serializers.ModelSerializer):
    char_name = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = LevelProg
        fields = ('id', 'episode', 'sheet', 'level', 'char_name')

    @staticmethod
    def get_char_name(instance):
        return instance.sheet.character.name

    @staticmethod
    def get_level(instance):
        return instance.sheet.get_level_verbose()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(LevelProgSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class VodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VodType
        fields = ('id', 'name')


class VodLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = VodLinks
        fields = ('id', 'episode', 'vod_type', 'link_key')


class EpisodeDetailSerializer(serializers.ModelSerializer):
    appearances = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    casts = serializers.SerializerMethodField()
    level_ups = serializers.SerializerMethodField()
    next_episode = serializers.SerializerMethodField()
    prev_episode = serializers.SerializerMethodField()
    rolls = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ('id', 'campaign', 'num', 'title', 'air_date','description', 'length', 'next_episode', 'prev_episode',
                  'first_half_start', 'first_half_end', 'second_half_start','second_half_end',
                  'rolls', 'appearances', 'level_ups', 'combat_encounters', 'vod_links', 'attendance', 'casts')
        depth = 1

    @staticmethod
    def get_appearances(instance):
        qs = instance.apperances.prefetch_related('apperance_type', 'character').order_by('character__name')
        return ApperanceSerializer(qs, many=True, fields=('apperance_type', 'character')).data

    @staticmethod
    def get_attendance(instance):
        qs = instance.attendance.prefetch_related('attendance_type', 'player').order_by('player__full_name')
        return AttendanceSerializer(qs, many=True, fields=('player', 'attendance_type')).data

    @staticmethod
    def get_level_ups(instance):
        qs = instance.level_ups.prefetch_related('sheet', 'sheet__classes', 'sheet__character').order_by('sheet__character__name')
        return LevelProgSerializer(qs, many=True, fields=('id', 'sheet', 'level', 'char_name')).data

    @staticmethod
    def get_rolls(instance):
        queryset = instance.rolls.prefetch_related('character', 'roll_type').order_by('timestamp')
        fields_wanted = ('id', 'timestamp', 'character', 'roll_type', 'natural_value', 'final_value', 'notes', 'damage','kill_count')
        if instance.campaign.num == 1 and (instance.num == 31 or instance.num == 33 or instance.num == 35):
            p1_queryset = queryset.filter(notes__startswith='p1')
            p1 = RollsSerializer(p1_queryset, many=True, fields=fields_wanted).data
            p2_queryset = queryset.filter(notes__startswith='p2')
            p2 = RollsSerializer(p2_queryset, many=True, fields=fields_wanted).data
            return list(chain(p1, p2))
        else:
            return RollsSerializer(queryset, many=True, fields=fields_wanted).data

    @staticmethod
    def get_casts(instance):
        queryset = instance.casts.prefetch_related('character', 'episode', 'spell').order_by('timestamp')
        if instance.campaign.num == 1 and (instance.num == 31 or instance.num == 33 or instance.num == 35):
            p1_queryset = queryset.filter(notes__startswith='p1')
            p1 = SpellCastInEpSerializer(p1_queryset, many=True).data
            p2_queryset = queryset.filter(notes__startswith='p2').order_by('timestamp')
            p2 = SpellCastInEpSerializer(p2_queryset, many=True).data
            return list(chain(p1, p2))
        else:
            return SpellCastInEpSerializer(queryset, many=True).data

    @staticmethod
    def get_next_episode(instance):
        if instance.num != instance.campaign.length:
            if instance.num == 11 and instance.campaign.num == 1:
                # campaign 1 episode 12 was some guide and isn't a core episode so it is skipped
                return Episode.objects.get(campaign=instance.campaign, num=13).id
            return Episode.objects.get(campaign=instance.campaign, num=(instance.num + 1)).id
        else:
            return None

    @staticmethod
    def get_prev_episode(instance):
        if instance.num != 1:
            if instance.num == 13 and instance.campaign.num == 1:
                # campaign 1 episode 12 was some guide and isn't a core episode so it is skipped
                return Episode.objects.get(campaign=instance.campaign, num=11).id

            return Episode.objects.get(campaign=instance.campaign, num=(instance.num - 1)).id
        else:
            return None

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('rolls', 'vod_links', 'apperances', 'level_ups')
        return queryset

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(EpisodeDetailSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

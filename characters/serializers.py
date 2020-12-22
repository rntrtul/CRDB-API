from rest_framework import serializers
from django.db.models import Sum, Count
from .models import Ability, AbilityScore, Alignment, Character, CharacterType, ClassTaken, SavingThrow, Skill, \
    SkillList, StatSheet
from spells.serializers import SpellSerializer
from episodes.serializers import LevelProgSerializer, ApperanceSerializer
from languages.serializers import LearnedLanguageSerializer
from items.serializers import WeaponOwnedSerializer
from spells.serializers import LearnedSpellSerializer
from episodes.models import Episode
from rolls.models import RollType


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ('id', 'name')


class AbilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityScore
        fields = ('id', 'ability', 'score')
        depth = 1


class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = ('id', 'name')


class CharacterSerializer(serializers.ModelSerializer):
    # roll_count = serializers.SerializerMethodField()
    class Meta:
        model = Character
        fields = ('id', 'full_name', 'name')

    @staticmethod
    def get_roll_count(self, instance):
        return instance.rolls.count()

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset


class CharacterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterType
        fields = ('id', 'name')


class CharacterTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterType
        fields = ('id', 'name', 'characters')
        depth = 1


class ClassTakenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTaken
        fields = ('id', 'class_id', 'level')
        depth = 1


class SavingThrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingThrow
        fields = ('id', 'ability', 'modifier', 'proficient')
        depth = 1


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'ability')


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillList
        fields = ('id', 'skill', 'modifier', 'proficient')
        depth = 1


class StatSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatSheet
        fields = ['id', 'character', 'level']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(StatSheetSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class StatSheetDetailSerializer(serializers.ModelSerializer):
    # skills = SkillListSerializer('skills', many=True)
    skills = serializers.SerializerMethodField()
    saving_throws = SavingThrowSerializer('saving_throws', many=True, read_only=True)
    ability_scores = AbilityScoreSerializer('ability_scores', many=True, read_only=True)
    learned_spells = LearnedSpellSerializer('learned_spells', many=True, read_only=True)
    classes = ClassTakenSerializer('classes', many=True, read_only=True)

    class Meta:
        model = StatSheet
        fields = ['ability_scores', 'saving_throws', 'skills', 'learned_spells', 'level_ups', 'languages',
                  'weapons_owned', 'classes',
                  'id', 'character', 'alignment', 'max_health', 'level', 'armour_class', 'speed', 'initiative_bonus',
                  'proficiency_bonus',
                  'hit_die', 'inspiration_die', 'equipment', 'features_traits', 'attacks', 'weapons', 'proficiencies',
                  'casting_ability',
                  'casting_class', 'spell_attack_bonus', 'spell_save', 'cantrips', 'slots_one', 'slots_two',
                  'slots_three', 'slots_four',
                  'slots_five', 'slots_six', 'slots_seven', 'slots_eight', 'slots_nine']
        depth = 1

    @staticmethod
    def get_skills(instance):
        ordered = instance.skills.prefetch_related("skill").order_by("skill")
        return SkillListSerializer(ordered, many=True, read_only=True).data

    @staticmethod
    def get_learned_spells(self, instance):
        queryset = instance.learned_spells.prefetch_related('spell')
        return LearnedSpellSerializer(queryset, many=True, read_only=True).data

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('ability_scores', 'saving_throws', 'learned_spells', 'skills')
        return queryset


class CharacterDetailSerializer(serializers.ModelSerializer):
    sheets = serializers.SerializerMethodField()
    appearances = serializers.SerializerMethodField()
    roll_counts = serializers.SerializerMethodField()
    damage_total = serializers.SerializerMethodField()
    top_roll_types = serializers.SerializerMethodField()
    kill_count = serializers.SerializerMethodField()
    nat_ones = serializers.SerializerMethodField()
    nat_twenty = serializers.SerializerMethodField()
    top_spells = serializers.SerializerMethodField()
    hdywt_count = serializers.SerializerMethodField()
    campaign = serializers.SerializerMethodField()
    ep_totals = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'full_name', 'name', 'race', 'player', 'char_type',
                  'sheets', 'appearances', 'roll_counts', 'damage_total',
                  'top_roll_types', 'kill_count', 'nat_ones', 'nat_twenty', 'top_spells', 'hdywt_count', 'campaign',
                  'ep_totals')
        depth = 1

    @staticmethod
    def get_appearances(instance):
        ep_list = []
        queryset = instance.apperances.prefetch_related('episode').order_by('episode__num')

        for app in queryset.all():
            ep_list.append({
                'episode': app.episode.id,
                'episode_title': app.episode.title,
                'episode_num': app.episode.num,
                'air date': app.episode.air_date,
            })
        return ep_list

    @staticmethod
    def get_campaign(instance):
        if instance.apperances.first() is None:
            return

        camp = instance.apperances.first().episode.campaign
        return {
            'number': camp.num,
            'length': camp.length,
            'name': camp.name
        }

    @staticmethod
    def get_ep_totals(instance):
        if instance.apperances.first() is None:
            return

        camp = instance.apperances.first().episode.campaign
        dmg = RollType.objects.get(name="Damage")

        eps = Episode.objects.filter(campaign=camp)
        casts_ep = eps.filter(casts__character=instance).annotate(char_casts=Count('casts')).order_by("num")
        rolls_ep = eps.filter(rolls__character=instance).annotate(char_rolls=Count('rolls')).order_by("num")
        dmg_dealt_ep = eps.filter(rolls__character=instance, rolls__roll_type=dmg).annotate(
            char_dd=Sum('rolls__final_value')).order_by('num')

        casts = [0] * camp.length
        rolls = [0] * camp.length
        dmg_dealt = [0] * camp.length

        for ep in casts_ep.values():
            casts[ep['num'] - 1] = ep['char_casts']

        for ep in rolls_ep.values():
            rolls[ep['num'] - 1] = ep['char_rolls']

        for ep in dmg_dealt_ep.values():
            dmg_dealt[ep['num'] - 1] = ep['char_dd']

        return {
            'rolls': rolls,
            'casts': casts,
            'dmg_dealt': dmg_dealt,
        }

    @staticmethod
    def get_sheets(instance):
        sheet_list = []
        queryset = instance.stat_sheets.order_by('-level')
        for sheet in queryset.all():
            sheet_list.append({
                'id': sheet.id,
                'sheet_level': sheet.level,
            })
        return sheet_list

    # make characterStatSerialier() so less initial data is loaded (maybe not if it is default view for character)
    # but if split then intial render will be faster and then stats will load(maybe?) even if stat is still default

    @staticmethod
    def get_roll_counts(instance):
        rolls = instance.rolls.prefetch_related('advantages_used').prefetch_related('advantages_used__type')
        adv_used = rolls.values_list('advantages_used')
        adv_dis = rolls.values_list('advantages_disregarded')
        return {
            'total': rolls.count(),
            'advantages': adv_used.filter(advantages_used__type__name='Advantage').count() +
                          adv_dis.filter(advantages_used__type__name='Advantage').count(),
            'disadvantages': adv_used.filter(advantages_used__type__name='Disadvantage').count() +
                             adv_dis.filter(advantages_used__type__name='Disadvantage').count(),
            'luck': adv_used.filter(advantages_used__type__name='Luck').count(),
            'fate': adv_used.filter(advantages_used__type__name='Fate').count(),
            'decahedron': adv_used.filter(advantages_used__type__name='Fragment of Possibility').count(),
        }

    @staticmethod
    def get_damage_total(instance):
        return instance.rolls.filter(roll_type__name='Damage').aggregate(Sum('final_value'))['final_value__sum']

    @staticmethod
    def get_top_roll_types(instance):
        return instance.rolls.values_list('roll_type__name').annotate(roll_type_count=Count('roll_type')).order_by(
            '-roll_type_count')[:10]

    @staticmethod
    def get_kill_count(instance):
        return instance.rolls.aggregate(Sum('kill_count'))['kill_count__sum']

    @staticmethod
    def get_nat_ones(instance):
        return instance.rolls.exclude(roll_type__name="Damage").filter(natural_value=1).count()

    @staticmethod
    def get_nat_twenty(instance):
        return instance.rolls.exclude(roll_type__name="Damage").filter(natural_value=20).count()

    @staticmethod
    def get_top_spells(instance):
        return {
            'total_count': instance.casts.count(),
            'list': instance.casts.values_list('spell__name').annotate(spell_count=Count('spell')).order_by(
                '-spell_count')[:10]
        }

    @staticmethod
    def get_hdywt_count(instance):
        return instance.rolls.filter(notes__contains="HDYWTDT").count()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('race', 'player', 'char_type')
        queryset = queryset.prefetch_related('stat_sheets', 'apperances')
        return queryset

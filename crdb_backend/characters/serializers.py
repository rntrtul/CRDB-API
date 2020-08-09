from rest_framework import serializers
from django.db.models import Sum, Count
from .models import Ability, AbilityScore, Alignment, Character, CharacterType, ClassTaken, SavingThrow, Skill, SkillList, StatSheet
from spells.serializers import SpellSerializer
from episodes.serializers import LevelProgSerializer, ApperanceSerializer
from languages.serializers import LearnedLanguageSerializer
from items.serializers import WeaponOwnedSerializer
from spells.serializers import LearnedSpellSerializer

class AbilitySerializer (serializers.ModelSerializer):
  class Meta:
    model = Ability
    fields = ('id', 'name')

class AbilityScoreSerializer (serializers.ModelSerializer):
  class Meta:
    model = AbilityScore
    fields = ('id', 'ability', 'score')
    depth = 1

class AlignmentSerializer (serializers.ModelSerializer):
  class Meta:
    model = Alignment
    fields = ('id', 'name')

class CharacterSerializer (serializers.ModelSerializer):
  roll_count = serializers.SerializerMethodField()
  class Meta:
    model = Character
    fields = ('id', 'full_name', 'name', 'roll_count')
  
  def get_roll_count(self,instance):
    return instance.rolls.count()
  
  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('rolls')
    return queryset

class CharacterTypeSerializer (serializers.ModelSerializer):
  class Meta:
    model = CharacterType
    fields = ('id', 'name')

class CharacterTypeDetailSerializer (serializers.ModelSerializer):
  class Meta:
    model = CharacterType
    fields = ('id', 'name', 'characters')
    depth = 1

class ClassTakenSerializer (serializers.ModelSerializer):
  class Meta:
    model = ClassTaken
    fields = ('id', 'class_id',  'level')
    depth = 1

class SavingThrowSerializer (serializers.ModelSerializer):
  class Meta:
    model = SavingThrow
    fields = ('id', 'ability', 'modifier', 'proficient')
    depth = 1

class SkillSerializer (serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = ('id', 'name', 'ability')


class SkillListSerializer (serializers.ModelSerializer):
  class Meta:
    model = SkillList
    fields = ('id', 'skill', 'modifier', 'proficient')
    depth = 1

class StatSheetSerializer (serializers.ModelSerializer):
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

class StatSheetDetailSerializer (serializers.ModelSerializer):
  #skills = SkillListSerializer('skills', many=True)
  skills = serializers.SerializerMethodField()
  saving_throws = SavingThrowSerializer('saving_throws', many=True, read_only=True)
  ability_scores = AbilityScoreSerializer('ability_scores', many=True, read_only=True)
  learned_spells = LearnedSpellSerializer('learned_spells', many=True, read_only=True)
  classes = ClassTakenSerializer('classes', many=True, read_only=True)
  
  class Meta:
    model = StatSheet
    fields = ['ability_scores', 'saving_throws', 'skills', 'learned_spells', 'level_ups', 'languages', 'weapons_owned', 'classes',
             'id', 'character', 'alignment', 'max_health', 'level', 'armour_class', 'speed', 'initiative_bonus','proficiency_bonus',
              'hit_die', 'inspiration_die', 'equipment', 'features_traits', 'attacks','weapons', 'proficiencies', 'casting_ability',
              'casting_class', 'spell_attack_bonus','spell_save', 'cantrips', 'slots_one', 'slots_two', 'slots_three','slots_four',
              'slots_five', 'slots_six', 'slots_seven', 'slots_eight', 'slots_nine']
    depth = 1

  def get_skills(self, instance):
    ordered = instance.skills.prefetch_related("skill").order_by("skill")
    return SkillListSerializer(ordered, many = True, read_only=True).data

  def get_learned_spells (self, instance):
    queryset = instance.learned_spells.prefetch_related('spell')
    return LearnedSpellSerializer(queryset, many=True, read_only=True).data

  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.prefetch_related('ability_scores', 'saving_throws', 'learned_spells', 'skills')
    return queryset

class CharacterDetailSerializer (serializers.ModelSerializer):
  sheets = serializers.SerializerMethodField()
  apperances = serializers.SerializerMethodField()
  roll_count = serializers.SerializerMethodField()
  damage_total = serializers.SerializerMethodField()
  top_roll_types = serializers.SerializerMethodField()
  kill_count = serializers.SerializerMethodField()
  nat_ones = serializers.SerializerMethodField()
  nat_twenty = serializers.SerializerMethodField()
  top_spells = serializers.SerializerMethodField()
  hdywt_count = serializers.SerializerMethodField()

  class Meta:
    model = Character
    fields = ('id', 'full_name', 'name', 'race', 'player', 'char_type',
              'sheets', 'apperances', 'roll_count', 'damage_total', 
              'top_roll_types', 'kill_count', 'nat_ones', 'nat_twenty', 'top_spells', 'hdywt_count')
    depth = 1
  
  def get_apperances(self,instance):
    ep_list = []
    queryset = instance.apperances.prefetch_related('episode').order_by('episode__num')
    for app in queryset.all():
      ep_list.append({
        'episode':app.episode.id, 
        'episode_title':app.episode.title,
        'episode_num': app.episode.num,
      })
    return ep_list

  def get_sheets(self,instance):
    sheet_list = []
    queryset= instance.stat_sheets.order_by('-level')
    for sheet in queryset.all():
      sheet_list.append({
        'id': sheet.id,
        'sheet_level': sheet.level,
      })
    return sheet_list
  #make characterStatSerialier() so less initial data is loaded (maybe keep since it is gonna be default view for character)
  # but if split then intial render will be faster and then stats will load(maybe?) even if stat is still default 
  def get_roll_count(self,instance):
    return instance.rolls.count()

  def get_damage_total(self, instance):
    return instance.rolls.filter(roll_type__name='Damage').aggregate(Sum('final_value'))

  def get_top_roll_types(self, instance):
    return instance.rolls.values_list('roll_type__name').annotate(roll_type_count=Count('roll_type')).order_by('-roll_type_count')[:10]

  def get_kill_count (self,instance):
    return instance.rolls.aggregate(Sum('kill_count'))
  
  def get_nat_ones (self,instance):
    return instance.rolls.exclude(roll_type__name="Damage").filter(natural_value=1).count()
  
  def get_nat_twenty (self, instance):
    return instance.rolls.exclude(roll_type__name="Damage").filter(natural_value=20).count()

  def get_top_spells (self,instance):
    return instance.casts.values_list('spell__name').annotate(spell_count=Count('spell')).order_by('-spell_count')[:10]

  def get_hdywt_count (self,instacne):
    return instacne.rolls.filter(notes__contains="HDYWTDT").count()
  
  @staticmethod
  def setup_eager_loading(queryset):
    queryset = queryset.select_related('race', 'player', 'char_type')
    queryset = queryset.prefetch_related('stat_sheets', 'apperances')
    return queryset
   
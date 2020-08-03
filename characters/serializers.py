from rest_framework import serializers
from .models import Ability, AbilityScore, Alignment, Character, CharacterType, ClassTaken, SavingThrow, Skill, SkillList, StatSheet
from spells.serializers import SpellSerializer
from episodes.serializers import LevelProgSerializer, ApperanceSerializer
from languages.serializers import LearnedLanguageSerializer
from items.serializers import WeaponOwnedSerializer

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
  class Meta:
    model = Character
    fields = ('id', 'full_name', 'name')

class CharacterTypeSerializer (serializers.ModelSerializer):
  class Meta:
    model = CharacterType
    fields = ('id', 'name')

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

class StatSheetDetailSerializer (serializers.ModelSerializer):
  class Meta:
    model = StatSheet
    fields = ['ability_scores', 'saving_throws', 'learned_spells', 'level_ups', 'languages', 'weapons_owned', 'classes',
             'id', 'character', 'alignment', 'max_health', 'level', 'armour_class', 'speed', 'initiative_bonus',
              'proficiency_bonus', 'hit_die', 'inspiration_die', 'equipment', 'features_traits', 'attacks',
              'weapons', 'proficiencies', 'casting_ability', 'casting_class', 'spell_attack_bonus',
              'spell_save', 'cantrips', 'slots_one', 'slots_two', 'slots_three', 'slots_four', 'slots_five',
              'slots_six', 'slots_seven', 'slots_eight', 'slots_nine']
    depth = 1

class CharacterDetailSerializer (serializers.ModelSerializer):
  sheets = StatSheetSerializer(source='stat_sheets', many=True)
  apperances = ApperanceSerializer('apperances', many=True)
  class Meta:
    model = Character
    fields = ('id', 'full_name', 'name', 'race', 'player', 'char_type',
              'sheets', 'apperances')
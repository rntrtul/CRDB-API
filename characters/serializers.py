from rest_framework import serializers
from .models import Ability, AbilityScore, Alignment, Character, CharacterType, ClassTaken, SavingThrow, Skill, SkillList, StatSheet
from spells.serializers import SpellSerializer
from episodes.serializers import LevelProgSerializer
from languages.serializers import LearnedLanguageSerializer
from items.serializers import WeaponOwnedSerializer

class AbilitySerializer (serializers.ModelSerializer):
  class Meta:
    model = Ability
    fields = ('id', 'name')

class AbilityScoreSerializer (serializers.ModelSerializer):
  class Meta:
    model = AbilityScore
    fields = ('id', 'ability', 'score', 'stat_sheet')

class AlignmentSerializer (serializers.ModelSerializer):
  class Meta:
    model = Alignment
    fields = ('id', 'name')

class CharacterSerializer (serializers.ModelSerializer):
  class Meta:
    model = Character
    fields = ('id', 'full_name', 'name', 'race', 'player', 'char_type')

class CharacterTypeSerializer (serializers.ModelSerializer):
  class Meta:
    model = CharacterType
    fields = ('id', 'name')

class ClassTakenSerializer (serializers.ModelSerializer):
  class Meta:
    model = ClassTaken
    fields = ('id', 'stat_sheet', 'class_id',  'level')

class SavingThrowSerializer (serializers.ModelSerializer):
  class Meta:
    model = SavingThrow
    fields = ('id', 'stat_sheet', 'ability', 'modifier', 'proficient')

class SkillSerializer (serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = ('id', 'name', 'ability')

class SkillListSerializer (serializers.ModelSerializer):
  class Meta:
    model = SkillList
    fields = ('id', 'stat_sheet', 'skill', 'modifier', 'proficient')

class StatSheetSerializer (serializers.ModelSerializer):
  class Meta:
    model = StatSheet
    fields = ['id', 'character', 'level']

class StatSheetDetailSerializer (serializers.ModelSerializer):
  scores = AbilityScoreSerializer(source ='ability_scores', many =True)
  saves = SavingThrowSerializer(source='saving_throws', many=True)
  spells = SpellSerializer(source='learned_spells', many=True)
  level_up = LevelProgSerializer(source='level_ups', many=True)
  langs = LearnedLanguageSerializer(source='languages', many=True)
  weapons= WeaponOwnedSerializer(source='weapons_owned', many=True)

  class Meta:
    model = StatSheet
    fields = ['scores', 'saves', 'spells', 'level_up', 'langs', 'weapons_owned',
             'id', 'character', 'alignment', 'max_health', 'level', 'armour_class', 'speed', 'initiative_bonus',
              'proficiency_bonus', 'hit_die', 'inspiration_die', 'equipment', 'features_traits', 'attacks',
              'weapons', 'proficiencies', 'casting_ability', 'casting_class', 'spell_attack_bonus',
              'spell_save', 'cantrips', 'slots_one', 'slots_two', 'slots_three', 'slots_four', 'slots_five',
              'slots_six', 'slots_seven', 'slots_eight', 'slots_nine']
    depth = 1


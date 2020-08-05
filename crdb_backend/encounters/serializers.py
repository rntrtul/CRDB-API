from rest_framework import serializers
from .models import CombatApperance, CombatEncounter, InitiativeOrder

class CombatEncounterSerializer (serializers.ModelSerializer):
  class Meta:
      model = CombatEncounter
      fields = ('id', 'episode', 'name', 'start', 'end', 'rounds', 'notes')

class CombatApperanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = CombatApperance
    fields = ('id', 'encounter', 'character')

class InitiativeOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = InitiativeOrder
    fields = ('id', 'encounter', 'character', 'roll', 'rank')

from rest_framework import serializers
from .models import Potion, PotionUsage, Weapon, WeaponDamage, WeaponOwned, WeaponUsage

class PotionSerializer (serializers.ModelSerializer):
  class Meta:
    model = Potion
    fields = ('id', 'name', 'description')

class PotionUsageSerializer (serializers.ModelSerializer):
  class Meta:
    model = PotionUsage
    fields = ('id', 'by', 'to', 'episode', 'potion', 'timestamp' , 'notes')

class WeaponSerializer (serializers.ModelSerializer):
  class Meta:
    model = Weapon
    fields = ('id', 'name', 'attack_bonus')


class WeaponDamageSerializer (serializers.ModelSerializer):
  class Meta:
    model = WeaponDamage
    fields = ('id', 'die_num', 'weapon', 'modifier', 'damage_type', 'die')

class WeaponOwnedSerializer (serializers.ModelSerializer):
  class Meta:
    model = WeaponOwned
    fields = ('id', 'sheet', 'weapon')


class WeaponUsageSerializer (serializers.ModelSerializer):
  class Meta:
    model = WeaponUsage
    fields = ('id', 'roll', 'weapon')


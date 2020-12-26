from rest_framework import serializers
from .models import Damage, DamageType


class DamageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Damage
        fields = ('id', 'roll', 'by', 'to', 'damage_type', 'points')


class DamageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DamageType
        fields = ('id', 'name')

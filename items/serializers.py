from rest_framework import serializers
from .models import Potion, PotionUsage, Weapon, WeaponDamage, WeaponOwned, WeaponUsage
from episodes.serializers import EpisodeDetailSerializer
from rolls.serializers import RollsSerializer
from django.db.models import Sum


class PotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Potion
        fields = ('id', 'name', 'description')


class PotionUsageSerializer(serializers.ModelSerializer):
    by = serializers.SerializerMethodField()
    to = serializers.SerializerMethodField()
    episode = EpisodeDetailSerializer('episode', fields=('id', 'campaign', 'num', 'vod_links'))

    class Meta:
        model = PotionUsage
        fields = ('id', 'by', 'to', 'episode', 'potion', 'timestamp', 'notes')

    @staticmethod
    def get_by(instance):
        return {
            'id': instance.by.id,
            'name': instance.by.name,
        }

    @staticmethod
    def get_to(instance):
        return {
            'id': instance.to.id,
            'name': instance.to.name,
        }

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(PotionUsageSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class PotionDetailSerializer(serializers.ModelSerializer):
    uses = serializers.SerializerMethodField()

    class Meta:
        model = Potion
        fields = ('id', 'name', 'description', 'uses')

    @staticmethod
    def get_uses(instance):
        qs = instance.uses.prefetch_related('by', 'episode', 'to', 'episode__campaign', 'episode__vod_links')
        return PotionUsageSerializer(qs, many=True, fields=('id', 'by', 'to', 'episode', 'timestamp', 'notes')).data


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ('id', 'name', 'attack_bonus')


class WeaponDamageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponDamage
        fields = ('id', 'die_num', 'weapon', 'modifier', 'damage_type', 'die')
        depth = 1

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(WeaponDamageSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class WeaponOwnedSerializer(serializers.ModelSerializer):
    sheet = serializers.SerializerMethodField()

    class Meta:
        model = WeaponOwned
        fields = ('id', 'weapon', 'sheet')

    def get_sheet(self, instance):
        character = instance.sheet.character
        return {
            'id': character.id,
            'name': character.name,
            'level': instance.sheet.get_level_verbose(),
        }


class WeaponUsageSerializer(serializers.ModelSerializer):
    roll = RollsSerializer('roll')

    class Meta:
        model = WeaponUsage
        fields = ('id', 'roll', 'weapon')


class WeaponDetailSerializer(serializers.ModelSerializer):
    uses = serializers.SerializerMethodField()
    owners = serializers.SerializerMethodField()
    damages = serializers.SerializerMethodField()
    dmg_total = serializers.SerializerMethodField()

    class Meta:
        model = Weapon
        fields = ('id', 'name', 'attack_bonus', 'damages', 'dmg_total', 'uses', 'owners')

    @staticmethod
    def get_uses(instance):
        qs = instance.uses.prefetch_related('roll', 'roll__ep', 'roll__character', 'roll__roll_type',
                                            'roll__ep__campaign', 'roll__ep__vod_links')
        qs = qs.order_by('roll__ep__campaign', 'roll__ep__num', 'roll__timestamp')
        return WeaponUsageSerializer(qs, many=True).data

    @staticmethod
    def get_owners(instance):
        qs = instance.owners.prefetch_related('sheet', 'sheet__character', 'sheet__classes', 'sheet__classes__class_id')
        return WeaponOwnedSerializer(qs, many=True).data

    @staticmethod
    def get_damages(instance):
        qs = instance.damages.prefetch_related('damage_type', 'die')
        return WeaponDamageSerializer(qs, many=True, fields=('die_num', 'modifier', 'damage_type', 'die')).data

    @staticmethod
    def get_dmg_total(instance):
        qs = instance.uses.prefetch_related('roll')
        return {
            'final_total': qs.aggregate(final_total=Sum('roll__final_value'))['final_total'],
            'nat_total': qs.aggregate(nat_total=Sum('roll__natural_value'))['nat_total'],
        }

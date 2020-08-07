from rest_framework import serializers
from .models import Episode, ApperanceType, Apperance, Attendance, AttendanceType, Live, LevelProg, VodLinks, VodType
from rolls.serializers import RollsSerializer, RollTypeSerializer, RollsListSerializer
from encounters.serializers import CombatEncounterSerializer
from itertools import chain

class EpisodeSerializer(serializers.ModelSerializer):
	is_live = serializers.SerializerMethodField()
	class Meta:
		model = Episode
		fields = ('id', 'campaign', 'num', 'title', 'length', 'is_live')
		depth = 1
		
	def get_is_live(self,instance):
		if instance.live_episodes.exists():
			return True
		else:
			return False

	def get_roll_count(self,instance):
		return instance.rolls.count()

	@staticmethod
	def setup_eager_loading(queryset):
		queryset = queryset.select_related('campaign')
		queryset = queryset.prefetch_related('live_episodes')
		return queryset
		
class ApperanceTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApperanceType
		fields = ('id', 'name')


class ApperanceSerializer(serializers.ModelSerializer):
	#ep_title = serializers.SerializerMethodField()

	class Meta:
		model = Apperance
		fields = ('id', 'episode', 'apperance_type', 'character')
		depth = 1

	def get_ep_title(self,instance):
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
	
	def get_char_name(self, instance):
		return instance.sheet.character.name
	
	def get_level(self, instance):
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
	attendance = AttendanceSerializer('attendance', many=True, fields=('player', 'attendance_type'))
	level_ups = LevelProgSerializer('level_ups', many=True, fields=('id', 'sheet', 'level', 'char_name'))
	rolls = serializers.SerializerMethodField()
	class Meta:
		model = Episode
		fields = ('id', 'campaign', 'num', 'title', 'air_date','description', 'length',
						 'first_half_start', 'first_half_end', 'second_half_start','second_half_end',
						 'rolls', 'apperances', 'level_ups', 'combat_encounters', 'vod_links', 'attendance')
		depth = 2
	
	def get_rolls(self,instance):
		if instance.campaign.num == 1 and (instance.num == 31 or instance.num == 33 or instance.num == 35):
			p1_queryset = instance.rolls.filter(notes__startswith='p1').order_by('time_stamp').values()
			p1 = RollsSerializer('rolls', many=True).setup_eager_loading(p1_queryset)
			p2_queryset = instance.rolls.filter(notes__startswith='p2').order_by('time_stamp').values()
			p2 = RollsSerializer('rolls', many=True).setup_eager_loading(p2_queryset)
			return list(chain(p1, p2))			
		else:
			queryset = instance.rolls.order_by('time_stamp').values()
			return RollsSerializer('rolls', many=True).setup_eager_loading(queryset)

	@staticmethod
	def setup_eager_loading(queryset):
		queryset = queryset.prefetch_related('rolls', 'vod_links', 'apperances', 'level_ups')
		return queryset
		
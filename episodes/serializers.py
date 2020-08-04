from rest_framework import serializers
from .models import Episode, ApperanceType, Apperance, Attendance, AttendanceType, Live, LevelProg, VodLinks, VodType
from rolls.serializers import RollsSerializer
from encounters.serializers import CombatEncounterSerializer

class EpisodeSerializer(serializers.ModelSerializer):
	#campaign_name = serializers.CharField(source='campaign.name', read_only=True)
	class Meta:
		model = Episode
		fields = ('id', 'campaign', 'num', 'title', 'length')
		
class ApperanceTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApperanceType
		fields = ('id', 'name')

class ApperanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Apperance
		fields = ('id', 'episode', 'apperance_type', 'character')

class AttendanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attendance
		fields = ('id', 'episode', 'attendance_type', 'player')
		depth = 1

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
	class Meta:
		model = LevelProg
		fields = ('id', 'episode', 'sheet', 'level')

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
	class Meta:
		model = Episode
		fields = ('id', 'campaign', 'num', 'title', 'air_date','description', 'length',
						 'first_half_start', 'first_half_end', 'second_half_start','second_half_end',
						 'rolls', 'apperances', 'level_ups', 'combat_encounters', 'vod_links', 'attendance')
		depth = 1
		
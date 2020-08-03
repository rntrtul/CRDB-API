from rest_framework import serializers
from .models import Episode, ApperanceType, Apperance, Attendance, AttendanceType, Live, LevelProg, VodLinks, VodType

class EpisodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Episode
		fields = ('id', 'campaign', 'num', 'title', 'air_date','description', 'length',
						'first_half_start', 'first_half_end', 'second_half_start','second_half_end')
		
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
from django.db import models
from datetime import datetime
from campaigns.models import Campaign
from characters.models import Character, StatSheet
from players.models import Player
import time

# Create your models here.
class Episode(models.Model):
  campaign = models.ForeignKey(Campaign, related_name='episodes', on_delete=models.CASCADE)
  num = models.IntegerField()
  title = models.TextField()
  air_date = models.DateField(auto_now_add=True, blank=True)
  description = models.TextField()
  length = models.IntegerField(default=0)
  first_half_start = models.IntegerField(default=0)
  first_half_end = models.IntegerField(default=0)
  second_half_start =  models.IntegerField(default=0,blank=True, null=True)
  second_half_end =  models.IntegerField(default=0,blank=True, null=True)

  def break_length (self):
     return self.second_half_start - self.first_half_end

  def first_half_length (self):
    return  self.first_half_end - self.first_half_start
  
  def second_half_length (self):
    return  self.second_half_end - self.second_half_start

  def gameplay_length (self):
    return self.first_half_length() + self.second_half_length()

class ApperanceType(models.Model):
  name = models.CharField(max_length=100)

class Apperance(models.Model):
  episode = models.ForeignKey(Episode, related_name='apperances', on_delete=models.CASCADE)
  apperance_type = models.ForeignKey(ApperanceType, related_name='apperances', on_delete=models.CASCADE)
  character = models.ForeignKey(Character, related_name='apperances', on_delete=models.CASCADE)

class LevelProg(models.Model):
  episode = models.ForeignKey(Episode, related_name='level_ups', on_delete=models.CASCADE)
  sheet = models.ForeignKey(StatSheet, related_name='level_ups', on_delete=models.CASCADE)
  level = models.IntegerField(default=0)

class AttendanceType(models.Model):
  name = models.TextField()

class Attendance(models.Model):
  episode= models.ForeignKey(Episode, related_name='attendance', on_delete=models.CASCADE)
  player = models.ForeignKey(Player, related_name='attendance', on_delete=models.CASCADE)
  attendance_type = models.ForeignKey(AttendanceType, related_name='attendances', on_delete=models.CASCADE)

class Live(models.Model):
  episode= models.ForeignKey(Episode, related_name='live_episodes', on_delete=models.CASCADE)
  venue = models.TextField()
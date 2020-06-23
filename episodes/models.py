from django.db import models
from datetime import datetime
from campaigns.models import Campaign

# Create your models here.
class Episode(models.Model):
  campaign = models.ForeignKey(Campaign, related_name='episodes', on_delete=models.CASCADE)
  num = models.IntegerField()
  title = models.TextField()
  air_date = models.DateField(auto_now_add=True, blank=True)
  description = models.TextField()
  length = models.IntegerField(default=0)
  game_start = models.IntegerField(default=0)
  break_start = models.IntegerField(default=0)
  break_end =  models.IntegerField(default=0)
  game_end =  models.IntegerField(default=0)
  
  def break_time (self):
    return self.break_end - self.break_start

  def first_half_time (self):
    return self.break_start - self. game_start
  
  def second_half_time (self):
    return (self.game_end - self.break_end)

  def game_time (self):
    return self.first_half_time() + self.second_half_time()
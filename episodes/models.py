from django.db import models
from datetime import datetime

# Create your models here.
class Campaign(models.Model):
  num = models.IntegerField(default=0)
  name = models.TextField()

class Episode(models.Model):
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  num = models.IntegerField()
  title = models.TextField()
  air_date = models.DateField(auto_now_add=True, blank=True)
  description = models.TextField()
  length = models.IntegerField(default=0)
  game_start = models.IntegerField(default=0)
  break_start = models.IntegerField(default=0)
  break_end =  models.IntegerField(default=0)
  game_end =  models.IntegerField(default=0)

  def game_time (self):
    return (self.game_end - self.break_end) + (self.break_start - self. game_start)
  
  def break_time (self):
    return self.break_end - self.break_start
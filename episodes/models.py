from django.db import models
from datetime import datetime
from campaigns.models import Campaign
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
  
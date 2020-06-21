from django.db import models

# Create your models here.
class Campaign(models.Model):
  num = models.IntegerField(default=0)
  name = models.TextField()

class Episode(models.Model):
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  number = models.IntegerField()
  title = models.TextField()
  airDate = models.DateField()
  description = models.TextField()
  length = models.IntegerField(default=0)
  gameStart = models.IntegerField(default=0)
  breakStart = models.IntegerField(default=0)
  breakEnd =  models.IntegerField(default=0)
  gameEnd =  models.IntegerField(default=0)

  def game_time (self):
    return (self.gameEnd - self.breakEnd) + (self.breakStart - self. gameStart)
  
  def break_time (self):
    return self.breakEnd - self.breakStart
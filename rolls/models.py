from django.db import models

# Create your models here.
class RollType(models.Model):
  name = models.CharField(max_length=100)

class Rolls(models.Model):
  time = models.IntegerField(default=0)
  naturalValue = models.IntegerField(default=0)
  finalValue = models.IntegerField(default=0)
  notes = models.CharField(max_length=200)
  rollType = models.ForeignKey(RollType,on_delete=models.CASCADE )
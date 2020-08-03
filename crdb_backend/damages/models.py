from django.db import models
from characters.models import Character
from rolls.models import Rolls

# Create your models here.
class DamageType(models.Model):
  name = models.TextField()

class Damage(models.Model):
  roll = models.ForeignKey(Rolls, related_name='damages', on_delete=models.CASCADE, null = True) #maybe make this null since some damage is not associated with roll
  by = models.ForeignKey(Character, related_name='damage_taken', on_delete=models.CASCADE, null=True)
  to = models.ForeignKey(Character, related_name='damage_dealt', on_delete=models.CASCADE)
  damage_type = models.ForeignKey(DamageType, related_name='damages', on_delete=models.CASCADE)
  points = models.IntegerField(default=-1)
from django.db import models
from characters.models import Character
from episodes.models import Episode
# Create your models here.
class Potion(models.Model):
  name = models.TextField()
  description = models.TextField(blank=True)

class PotionUsage(models.Model):
  by = models.ForeignKey(Character, related_name='potions_administered', on_delete=models.CASCADE)
  to = models.ForeignKey(Character, related_name='potions_consumed', on_delete=models.CASCADE)
  episode = models.ForeignKey(Episode, related_name='potions', on_delete=models.CASCADE)
  potion = models.ForeignKey(Potion, related_name='uses', on_delete=models.CASCADE)
  timestamp = models.IntegerField(default=0)
  notes = models.TextField(blank=True)
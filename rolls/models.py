import platform
import time

from django.db import models

from characters.models import Character
from episodes.models import Episode


# Create your models here.
class Die(models.Model):
    sides = models.IntegerField()


# add boolean fields, skill, save, ability, damage
class RollType(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


# maybe add advantage type table instead of advantage field
class Rolls(models.Model):
    # todo: rename ep to episode
    timestamp = models.IntegerField(default=0)
    natural_value = models.IntegerField(default=0, null=True)
    final_value = models.IntegerField(default=0, null=True)
    notes = models.TextField()
    damage = models.TextField(blank=True)
    roll_type = models.ForeignKey(RollType, related_name='rolls', on_delete=models.CASCADE)
    ep = models.ForeignKey(Episode, related_name='rolls', on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name='rolls', on_delete=models.CASCADE)
    kill_count = models.IntegerField(default=0)  # might be a temp column until, all kills in kills table

    def time_formated(self):
        if platform.system() == 'Linux':
            return time.strftime("%-H:%M:%S", time.gmtime(self.timestamp))
        else:
            return time.strftime("%#H:%M:%S", time.gmtime(self.timestamp))


class AdvantageType(models.Model):
    name = models.TextField()


class Advantage(models.Model):
    type = models.ForeignKey(AdvantageType, related_name='rolls', on_delete=models.CASCADE)
    used = models.ForeignKey(Rolls, related_name='advantages_used', on_delete=models.CASCADE, blank=True, null=True)
    disregarded = models.ForeignKey(Rolls, related_name='advantages_disregarded', on_delete=models.CASCADE, blank=True,
                                    null=True)
    # null since some are just single advantage rolls


class Kill(models.Model):
    roll = models.ForeignKey(Rolls, related_name='kills', on_delete=models.CASCADE)  # can be null for PC killed by DM
    killed = models.ForeignKey(Character, related_name='deaths', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

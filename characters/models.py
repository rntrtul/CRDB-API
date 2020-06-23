from django.db import models
from races.models import Race
from classes.models import Class

# Create your models here.
class CharacterType(models.Model):
  name = models.CharField(max_length=50)

class Character(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100, blank=True)
  middle_name = models.CharField(max_length=100, blank=True)
  race = models.ForeignKey(Race, related_name='characters', on_delete=models.CASCADE)
  char_type = models.ForeignKey(CharacterType, related_name='list_of_chars', on_delete=models.CASCADE)

  def is_multiClass(self):  
    if self.classes.count() == 1:
      return False
    else:
      return True

class ClassTaken(models.Model):
  character = models.ForeignKey(Character,related_name='classes', on_delete=models.CASCADE)
  class_id = models.ForeignKey(Class, related_name = 'characters', on_delete=models.CASCADE)
  level = models.IntegerField(default=0)
from django.db import models
from characters.models import StatSheet

# Create your models here.
class Language(models.Model):
  #maybe add what script language is written in (serpate model)
  name = models.CharField(max_length=100)

class LearnedLanguage (models.Model):
  language = models.ForeignKey(Language, related_name='known_by', on_delete=models.CASCADE)
  sheet = models.ForeignKey(StatSheet, related_name='languages', on_delete=models.CASCADE)

from django.db import models

# Create your models here.
# probably move level_prog here
# add spell casting ability here nullable
class Class(models.Model):
  name = models.CharField(max_length=100)
  #spell_casting_ability = models.ForeignKey(Ability, relared_name='classes_spell_casting', on_delete=models.CASCADE)
from django.db import models

# Create your models here.
class Campaign(models.Model):
  num = models.IntegerField(default=0)
  name = models.TextField()
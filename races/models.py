from django.db import models


# Create your models here.
class Race(models.Model):
    name = models.CharField(max_length=100)

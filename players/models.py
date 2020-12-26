from django.db import models


# Create your models here.
class Player(models.Model):
    full_name = models.TextField()

    def first_name(self):
        return self.full_name.split(' ')[0]

    def last_name(self):
        return self.full_name.split(' ')[-1]

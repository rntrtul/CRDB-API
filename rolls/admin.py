from django.contrib import admin
from .models import RollType, Rolls
# Register your models here.

class RollTypeInLine(admin.StackedInline):
  model = RollType
  extra = 1

class RollsAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['notes', 'timeStamp']}),
    ('Die Roll', {'fields': ['finalValue', 'naturalValue', 'rollType']}),
  ]

admin.site.register(RollType)
admin.site.register(Rolls, RollsAdmin)
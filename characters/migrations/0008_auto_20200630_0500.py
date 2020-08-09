# Generated by Django 3.0.6 on 2020-06-30 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0007_auto_20200630_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingthrow',
            name='profcient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statsheet',
            name='attacks',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='statsheet',
            name='proficiencies',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='statsheet',
            name='spell_save',
            field=models.IntegerField(default=0),
        ),
    ]
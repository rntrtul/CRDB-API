# Generated by Django 3.0.6 on 2020-07-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0016_auto_20200702_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='cantrip',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='spell',
            name='level',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

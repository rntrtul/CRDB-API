# Generated by Django 3.0.6 on 2020-07-25 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolls', '0016_auto_20200723_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='kill',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]

# Generated by Django 3.1 on 2020-09-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='length',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

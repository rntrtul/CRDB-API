# Generated by Django 3.0.6 on 2020-06-22 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
        ('rolls', '0009_auto_20200622_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolls',
            name='character',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rolls', to='characters.Character'),
            preserve_default=False,
        ),
    ]

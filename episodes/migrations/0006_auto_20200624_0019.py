# Generated by Django 3.0.6 on 2020-06-24 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0005_auto_20200623_2202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='break_end',
            new_name='first_half_end',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='break_start',
            new_name='first_half_start',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='game_end',
            new_name='second_half_end',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='game_start',
            new_name='second_half_start',
        ),
    ]

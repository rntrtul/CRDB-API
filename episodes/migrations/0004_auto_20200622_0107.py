# Generated by Django 3.0.6 on 2020-06-22 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0003_auto_20200621_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='airDate',
            new_name='air_date',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='breakEnd',
            new_name='break_end',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='breakStart',
            new_name='break_start',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='gameEnd',
            new_name='game_end',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='gameStart',
            new_name='game_start',
        ),
    ]

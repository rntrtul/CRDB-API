# Generated by Django 3.0.8 on 2020-08-03 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0022_statsheet_level'),
        ('items', '0007_auto_20200802_0116'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeaponeOwned',
            new_name='WeaponOwned',
        ),
    ]
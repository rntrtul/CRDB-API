# Generated by Django 3.0.6 on 2020-06-22 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolls', '0007_auto_20200622_0056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rolls',
            old_name='finalValue',
            new_name='final_value',
        ),
        migrations.RenameField(
            model_name='rolls',
            old_name='naturalValue',
            new_name='natural_value',
        ),
        migrations.RenameField(
            model_name='rolls',
            old_name='rollType',
            new_name='roll_type',
        ),
    ]
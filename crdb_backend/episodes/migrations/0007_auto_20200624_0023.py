# Generated by Django 3.0.6 on 2020-06-24 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0006_auto_20200624_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='second_half_end',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='second_half_start',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
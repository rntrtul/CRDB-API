# Generated by Django 3.0.6 on 2020-06-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolls', '0002_auto_20200620_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolls',
            name='notes',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='rolltype',
            name='name',
            field=models.TextField(),
        ),
    ]
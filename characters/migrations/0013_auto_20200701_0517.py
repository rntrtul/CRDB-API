# Generated by Django 3.0.6 on 2020-07-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0012_auto_20200701_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statsheet',
            name='spell_attack_bonus',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='statsheet',
            name='spell_save',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
# Generated by Django 3.0.8 on 2020-08-03 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rolls', '0017_kill_count'),
        ('characters', '0022_statsheet_level'),
        ('damages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damage',
            name='by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='damage_taken', to='characters.Character'),
        ),
        migrations.AlterField(
            model_name='damage',
            name='roll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='damages', to='rolls.Rolls'),
        ),
    ]

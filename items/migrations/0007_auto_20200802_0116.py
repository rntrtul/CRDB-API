# Generated by Django 3.0.6 on 2020-08-02 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('damages', '0001_initial'),
        ('items', '0006_weaponusage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weapondamage',
            name='damage_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weapons', to='damages.DamageType'),
        ),
        migrations.DeleteModel(
            name='DamageType',
        ),
    ]
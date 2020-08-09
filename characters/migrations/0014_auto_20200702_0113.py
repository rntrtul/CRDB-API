# Generated by Django 3.0.6 on 2020-07-02 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
        ('characters', '0013_auto_20200701_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='full_name',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='character',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='character',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='players.Player'),
            preserve_default=False,
        ),
    ]
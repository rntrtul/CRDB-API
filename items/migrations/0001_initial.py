# Generated by Django 3.0.6 on 2020-07-02 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0015_auto_20200702_0341'),
        ('episodes', '0010_levelprog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Potion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PotionUseage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='potions_administered', to='characters.Character')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='potions', to='episodes.Episode')),
                ('potion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uses', to='items.Potion')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='potions_consumed', to='characters.Character')),
            ],
        ),
    ]

# Generated by Django 3.0.6 on 2020-07-24 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0012_auto_20200716_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='VodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VodLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_key', models.TextField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vod_links', to='episodes.Episode')),
                ('vod_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='episodes.VodType')),
            ],
        ),
    ]

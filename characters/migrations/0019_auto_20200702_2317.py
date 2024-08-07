# Generated by Django 3.0.6 on 2020-07-02 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0018_auto_20200702_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnedSpells',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learned_spells_poo', to='characters.StatSheet')),
                ('spell_old', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='known_by_poo', to='characters.Spells')),
            ],
        ),
        migrations.DeleteModel(
            name='LearnedSpell',
        ),
    ]

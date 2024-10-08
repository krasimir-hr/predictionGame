# Generated by Django 5.0.4 on 2024-09-19 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0013_rename_full_name_team_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='game_type',
            field=models.CharField(blank=True, choices=[('BO1', 'Best of 1'), ('BO3', 'Best of 3'), ('BO5', 'Best of 5')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_team_1', to='tournament.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_team_2', to='tournament.team'),
        ),
    ]

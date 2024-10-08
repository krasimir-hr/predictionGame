# Generated by Django 5.0.4 on 2024-09-19 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0015_rename_game_type_match_match_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='mvp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_1_bans',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_1_picks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_1_players_stats',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_2_bans',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_2_picks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_2_players_stats',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]

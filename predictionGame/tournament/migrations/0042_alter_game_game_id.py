# Generated by Django 5.0.4 on 2025-06-22 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0041_rename_side_selection_game_team_1_side_selection_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_id',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]

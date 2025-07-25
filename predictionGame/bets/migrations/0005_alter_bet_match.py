# Generated by Django 5.0.4 on 2025-06-23 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0004_rename_highest_winrate_champion_wildcards_most_picked_bot_and_more'),
        ('tournament', '0044_alter_champion_name_alter_item_name_alter_rune_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='tournament.match'),
        ),
    ]

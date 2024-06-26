# Generated by Django 5.0.4 on 2024-04-26 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0002_bet_bet_points'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wildcards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('most_picked_champion', models.CharField(max_length=50)),
                ('most_banned_champion', models.CharField(max_length=50)),
                ('highest_winrate_champion', models.CharField(max_length=50)),
                ('player_with_most_kills', models.CharField(max_length=50)),
                ('player_with_most_assists', models.CharField(max_length=50)),
                ('player_with_most_deaths', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

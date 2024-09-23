# Generated by Django 5.0.4 on 2024-09-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0003_wildcards'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wildcards',
            old_name='highest_winrate_champion',
            new_name='most_picked_bot',
        ),
        migrations.RenameField(
            model_name='wildcards',
            old_name='most_picked_champion',
            new_name='most_picked_jgl',
        ),
        migrations.AddField(
            model_name='wildcards',
            name='most_picked_mid',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wildcards',
            name='most_picked_sup',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wildcards',
            name='most_picked_top',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wildcards',
            name='tournament_winner',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_alter_match_team1_score_alter_match_team2_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team1_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

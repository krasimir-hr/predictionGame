# Generated by Django 5.0.4 on 2024-04-25 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_alter_match_match_timedate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterField(
            model_name='match',
            name='match_timedate',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 30, 11, 0)),
        ),
    ]

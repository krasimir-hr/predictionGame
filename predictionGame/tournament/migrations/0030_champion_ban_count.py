# Generated by Django 5.0.4 on 2024-09-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0029_rename_picks_pick'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='ban_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-09-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0031_alter_champion_ban_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='ban_count',
            field=models.IntegerField(default=0),
        ),
    ]

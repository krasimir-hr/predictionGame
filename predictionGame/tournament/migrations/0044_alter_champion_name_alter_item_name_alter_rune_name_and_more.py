# Generated by Django 5.0.4 on 2025-06-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0043_item_rune_summonerspell_remove_champion_ban_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='rune',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='summonerspell',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]

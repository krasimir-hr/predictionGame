# Generated by Django 5.0.4 on 2024-09-23 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0028_picks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Picks',
            new_name='Pick',
        ),
    ]
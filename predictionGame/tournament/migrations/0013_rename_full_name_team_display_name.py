# Generated by Django 5.0.4 on 2024-09-19 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0012_alter_match_match_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='full_name',
            new_name='display_name',
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-27 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='edited_username',
        ),
    ]

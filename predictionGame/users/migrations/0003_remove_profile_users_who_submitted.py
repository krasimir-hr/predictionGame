# Generated by Django 5.0.4 on 2024-04-25 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_users_who_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='users_who_submitted',
        ),
    ]

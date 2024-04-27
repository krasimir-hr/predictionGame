# Generated by Django 5.0.4 on 2024-04-25 15:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_alter_match_options_alter_match_match_timedate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='users_who_submitted',
            field=models.ManyToManyField(blank=True, related_name='matches_for_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='match_timedate',
            field=models.DateTimeField(default="2024-04-30T11:00:00"),
            preserve_default=False,
        ),
    ]

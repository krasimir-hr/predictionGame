# Generated by Django 5.0.4 on 2024-04-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.URLField(blank=True, default='https://i.pinimg.com/564x/c0/c8/17/c0c8178e509b2c6ec222408e527ba861.jpg', null=True),
        ),
    ]
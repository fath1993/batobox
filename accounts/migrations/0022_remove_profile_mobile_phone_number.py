# Generated by Django 4.2.7 on 2024-01-04 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_profile_first_name_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile_phone_number',
        ),
    ]

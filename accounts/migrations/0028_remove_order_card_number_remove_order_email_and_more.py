# Generated by Django 4.2.7 on 2024-01-31 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_order_email_profile_unseen_ticket_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='isbn',
        ),
        migrations.RemoveField(
            model_name='order',
            name='landline',
        ),
        migrations.RemoveField(
            model_name='order',
            name='mobile_phone_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='national_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
    ]

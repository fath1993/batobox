# Generated by Django 4.2.7 on 2024-01-25 12:29

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_requestedproduct_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedproduct',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی'),
        ),
    ]

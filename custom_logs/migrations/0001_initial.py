# Generated by Django 4.2.2 on 2023-07-01 16:43

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='no description', verbose_name='توضیحات ')),
                ('log_level', models.CharField(choices=[('DEBUG', 'DEBUG'), ('INFO', 'INFO')], default='INFO', max_length=255, verbose_name='سطح لوگ ')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'لوگ',
                'verbose_name_plural': 'لوگ ها',
                'ordering': ['-created_at'],
            },
        ),
    ]

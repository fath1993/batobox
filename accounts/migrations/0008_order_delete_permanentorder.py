# Generated by Django 4.2.7 on 2023-12-11 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_profile_temp_card_delete_temporarycart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products_details', models.TextField(verbose_name='محصولات نهایی شده')),
                ('payable_amount_in_tomans', models.PositiveIntegerField(default=0, verbose_name='مبلغ قابل پرداخت')),
                ('all_time_payed_amount_in_tomans', models.PositiveIntegerField(default=0, verbose_name='مبلغ پرداخت شده تا کنون')),
                ('order_status', models.IntegerField(choices=[(1, 'در حال بررسی'), (2, 'پرداخت شده و در انتظار بررسی'), (3, 'در انتظار پرداخت مبلغ اصلاحیه'), (4, 'درحال آماده سازی'), (5, 'ارسال شده'), (6, 'لغو شده'), (7, 'ارسال به ایران'), (8, 'در گمرک'), (9, 'در انبار باتوباکس')], default=1, verbose_name='وضعیت سفارش')),
                ('payment_history', models.TextField(blank=True, null=True, verbose_name='سابقه پرداخت')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_permanent_order', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش ها',
            },
        ),
        migrations.DeleteModel(
            name='PermanentOrder',
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-02 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0011_alter_requestedproduct_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestedproduct',
            name='asin',
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='batobox_commission_percentage',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='درصد کارمزد باتوباکس با توجه به وزن'),
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='batobox_currency_exchange_fee_percentage',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='درصد کارمزد باتوباکس برای تبدیل ارز'),
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='batobox_final_price_in_toman',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت نهایی به تومان'),
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='batobox_shipping_price_in_toman',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت حمل و نقل به تومان'),
        ),
        migrations.AlterField(
            model_name='requestedproduct',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت به واحد ارز'),
        ),
        migrations.CreateModel(
            name='ProductCalculatorAccessHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط')),
            ],
            options={
                'verbose_name': 'سابقه دسترسی به محاسبه گر محصولات',
                'verbose_name_plural': 'سوابق دسترسی به محاسبه گر محصولات',
                'ordering': ['-created_at'],
            },
        ),
    ]

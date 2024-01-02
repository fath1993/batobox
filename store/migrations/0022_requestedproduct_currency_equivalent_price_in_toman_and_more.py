# Generated by Django 4.2.7 on 2023-12-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_requestedproduct_batobox_currency_exchange_commission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedproduct',
            name='currency_equivalent_price_in_toman',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت واحد ارز به تومان'),
        ),
        migrations.AlterField(
            model_name='batoboxcurrencyexchangecommission',
            name='unique_code',
            field=models.CharField(editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
        migrations.AlterField(
            model_name='batoboxshipping',
            name='unique_code',
            field=models.CharField(editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='unique_code',
            field=models.CharField(editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-17 18:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_batoboxcurrencyexchangecommission_unique_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batoboxcurrencyexchangecommission',
            name='unique_code',
            field=models.CharField(default=uuid.UUID('1b93e028-5381-495a-9577-c1bf41dc47c1'), editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
        migrations.AlterField(
            model_name='batoboxshipping',
            name='unique_code',
            field=models.CharField(default=uuid.UUID('902fa650-f99a-4fd6-8ca4-8a3058e15166'), editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='unique_code',
            field=models.CharField(default=uuid.UUID('9addea26-32fd-441f-b6c0-725f2f95661f'), editable=False, max_length=255, verbose_name='کد یکتا'),
        ),
    ]

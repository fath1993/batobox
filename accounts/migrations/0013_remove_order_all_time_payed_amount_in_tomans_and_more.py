# Generated by Django 4.2.7 on 2023-12-18 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_order_user_order_created_by_order_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='all_time_payed_amount_in_tomans',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payable_amount_in_tomans',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_history',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AddField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.order', verbose_name='سفارش'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('pending', 'پرداخت نشده'), ('done', 'پرداخت شده')], default='pending', max_length=255, verbose_name='وضعیت'),
        ),
    ]

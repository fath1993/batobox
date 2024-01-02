# Generated by Django 4.2.7 on 2023-12-08 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_rainforestapiaccesshistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rainforestapiaccesshistory',
            options={'ordering': ['-created_at'], 'verbose_name': 'سابقه دسترسی به rainforest api', 'verbose_name_plural': 'سوابق دسترسی به rainforest api'},
        ),
        migrations.RemoveField(
            model_name='batoboxcommission',
            name='maximum_shipping_price_in_toman',
        ),
        migrations.RemoveField(
            model_name='batoboxcommission',
            name='minimum_shipping_price_in_toman',
        ),
        migrations.AddField(
            model_name='batoboxcommission',
            name='currency',
            field=models.CharField(default=1, max_length=255, verbose_name='کمیسون مرتبط به ارز با نماد'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='batoboxcommission',
            name='price',
            field=models.PositiveIntegerField(default=1, verbose_name='مبلغ به واحد ارز'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='batoboxcommission',
            name='maximum_commission_percentage',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='بیشترین درصد کارمزد باتوباکس'),
        ),
        migrations.AlterField(
            model_name='batoboxcommission',
            name='minimum_commission_percentage',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='کمترین درصد کارمزد باتوباکس'),
        ),
    ]

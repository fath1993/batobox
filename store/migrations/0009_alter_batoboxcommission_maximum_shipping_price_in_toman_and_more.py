# Generated by Django 4.2.7 on 2023-12-01 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_requestedproduct_remove_category_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batoboxcommission',
            name='maximum_shipping_price_in_toman',
            field=models.PositiveIntegerField(verbose_name='بیشترین هزینه حمل باتوباکس بر اساس تومان'),
        ),
        migrations.AlterField(
            model_name='batoboxcommission',
            name='minimum_shipping_price_in_toman',
            field=models.PositiveIntegerField(verbose_name='کمترین هزینه حمل باتوباکس بر اساس تومان'),
        ),
        migrations.AlterField(
            model_name='batoboxcommission',
            name='weight_from',
            field=models.PositiveIntegerField(verbose_name='وزن از (واحد گرم)'),
        ),
        migrations.AlterField(
            model_name='batoboxcommission',
            name='weight_to',
            field=models.PositiveIntegerField(verbose_name='وزن تا (واحد گرم)'),
        ),
    ]

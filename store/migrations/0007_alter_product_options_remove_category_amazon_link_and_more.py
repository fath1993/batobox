# Generated by Django 4.2.7 on 2023-12-01 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0004_amazonproduct'),
        ('store', '0006_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.RemoveField(
            model_name='category',
            name='amazon_link',
        ),
        migrations.RemoveField(
            model_name='product',
            name='amazon_product_root_domain',
        ),
        migrations.RemoveField(
            model_name='product',
            name='asin',
        ),
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='base_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='documents',
        ),
        migrations.RemoveField(
            model_name='product',
            name='feature_bullets',
        ),
        migrations.RemoveField(
            model_name='product',
            name='final_price_in_toman',
        ),
        migrations.RemoveField(
            model_name='product',
            name='get_new_details_from_rainforest_api',
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_product_available',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_product_special',
        ),
        migrations.RemoveField(
            model_name='product',
            name='main_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_brand_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_main_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_root_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating_score',
        ),
        migrations.RemoveField(
            model_name='product',
            name='shipping_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug_title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title_fa',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user_rating_count',
        ),
        migrations.AddField(
            model_name='product',
            name='amazon_related_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='amazon.amazonproduct', verbose_name='محصول مرتبط آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(default=1, max_length=255, verbose_name='لینک'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=1, verbose_name='قیمت'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.currency', verbose_name='ارز'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=1, verbose_name='وزن به گرم'),
            preserve_default=False,
        ),
    ]

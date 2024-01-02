# Generated by Django 4.2.7 on 2023-12-01 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0008_remove_amazonproduct_get_new_details_from_rainforest_api'),
        ('store', '0010_requestedproduct_asin_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestedproduct',
            options={'verbose_name': 'درخواست محصول', 'verbose_name_plural': 'درخواست های محصولات'},
        ),
        migrations.AlterField(
            model_name='requestedproduct',
            name='amazon_related_product',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='amazon.amazonproduct', verbose_name='محصول مرتبط آمازون'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
        ('store', '0003_product_productdetail_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatoboxCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_from', models.FloatField(verbose_name='وزن از (واحد گرم)')),
                ('weight_to', models.FloatField(verbose_name='وزن تا (واحد گرم)')),
                ('minimum_commission_percentage', models.PositiveSmallIntegerField(verbose_name='کمترین درصد کارمزد باتوباکس')),
                ('maximum_commission_percentage', models.PositiveSmallIntegerField(verbose_name='بیشترین درصد کارمزد باتوباکس')),
                ('minimum_shipping_price_in_toman', models.FloatField(verbose_name='کمترین هزینه حمل باتوباکس بر اساس تومان')),
                ('maximum_shipping_price_in_toman', models.FloatField(verbose_name='بیشترین هزینه حمل باتوباکس بر اساس تومان')),
            ],
            options={
                'verbose_name': 'کارمزد باتوباکس',
                'verbose_name_plural': 'کارمزد های باتوباکس',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('badge', models.CharField(max_length=255, verbose_name='نماد')),
                ('currency_equivalent_price_in_toman', models.FloatField(blank=True, null=True, verbose_name='قیمت پایه واحد ارز به تومان')),
                ('exchange_fee_percentage', models.FloatField(blank=True, null=True, verbose_name='درصد کارمزد تبدیل')),
                ('price_in_toman', models.FloatField(blank=True, editable=False, null=True, verbose_name='قیمت نهایی واحد ارز به تومان')),
            ],
            options={
                'verbose_name': 'ارز',
                'verbose_name_plural': 'ارز ها',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=255, verbose_name='عنوان فارسی')),
                ('title_en', models.CharField(max_length=255, verbose_name='عنوان انگلیسی')),
                ('title_slug', models.SlugField(allow_unicode=True, blank=True, editable=False, max_length=255, null=True, verbose_name='اسلاگ عنوان')),
            ],
            options={
                'verbose_name': 'کلمه کلیدی',
                'verbose_name_plural': 'کلمات کلیدی',
            },
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='link',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_fa',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_slug',
        ),
        migrations.RemoveField(
            model_name='category',
            name='seo_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='seo_keywords',
        ),
        migrations.RemoveField(
            model_name='category',
            name='seo_title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='batobox_delivery',
        ),
        migrations.RemoveField(
            model_name='product',
            name='batobox_fee',
        ),
        migrations.RemoveField(
            model_name='product',
            name='delivery_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_link',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_fa',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_toman',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_uae',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller_link',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug_name',
        ),
        migrations.AddField(
            model_name='category',
            name='amazon_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(default=1, max_length=255, verbose_name='عنوان انگلیسی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='title_fa',
            field=models.CharField(default=1, max_length=255, verbose_name='عنوان فارسی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='title_slug',
            field=models.SlugField(allow_unicode=True, blank=True, editable=False, max_length=255, null=True, verbose_name='اسلاگ عنوان'),
        ),
        migrations.AddField(
            model_name='product',
            name='amazon_product_root_domain',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='لینک کشور-محصول آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='asin',
            field=models.CharField(default=1, max_length=255, verbose_name='ASIN'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.TextField(blank=True, null=True, verbose_name='امکانات'),
        ),
        migrations.AddField(
            model_name='product',
            name='base_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='قیمت پایه'),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='product_categories', to='store.category', verbose_name='دسته ها'),
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='ارز'),
        ),
        migrations.AddField(
            model_name='product',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='product_documents', to='storage.storage', verbose_name='مستندات'),
        ),
        migrations.AddField(
            model_name='product',
            name='feature_bullets',
            field=models.TextField(blank=True, null=True, verbose_name='ویژگی های کلیدی'),
        ),
        migrations.AddField(
            model_name='product',
            name='final_price_in_toman',
            field=models.FloatField(blank=True, null=True, verbose_name='هزینه نهایی محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='get_new_details_from_rainforest_api',
            field=models.BooleanField(default=False, verbose_name='دریافت اطلاعات جدید از rainforest api'),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='product_images', to='storage.storage', verbose_name='تصاویر'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_product_available',
            field=models.BooleanField(default=True, verbose_name='محصول فعال'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_product_special',
            field=models.BooleanField(default=False, verbose_name='محصول ویژه'),
        ),
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='product-image/', verbose_name='تصویر اصلی محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_brand_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='لینک برند محصول در آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_main_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='لینک اصلی محصول در آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_root_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='لینک ریشه محصول در آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نوع محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='rating_score',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='امتیاز محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='shipping_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='قیمت پایه حمل و نقل از آمازون'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug_title',
            field=models.SlugField(allow_unicode=True, blank=True, editable=False, max_length=255, null=True, verbose_name='اسلاگ عنوان'),
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.TextField(blank=True, null=True, verbose_name='مشخصات'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان انگلیسی'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_fa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان فارسی'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_rating_count',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='تعداد امتیاز دهندگان به محصول'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_tree',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='درخت رابطه'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='عنوان فارسی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='وزن بر اساس گرم'),
        ),
        migrations.DeleteModel(
            name='ProductDetail',
        ),
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='product_keywords', to='store.keyword', verbose_name='کلمات کلیدی'),
        ),
    ]

import json
import threading
from django.core.exceptions import ValidationError
from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django_jalali.db import models as jmodel
from django.utils.text import slugify

from storage.models import Storage


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='parent_category', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='دسته مادر')
    parent_tree = models.TextField(null=True, blank=True, editable=False, verbose_name='درخت رابطه')
    title_fa = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان فارسی')
    title_en = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان انگلیسی')
    title_slug = models.SlugField(max_length=255, null=True, blank=True, allow_unicode=True, editable=False,
                                  verbose_name='اسلاگ عنوان')
    cat_image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='تصویر دسته')

    def __str__(self):
        return self.title_fa

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'


class Keyword(models.Model):
    title_fa = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان فارسی')
    title_en = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان انگلیسی')
    title_slug = models.SlugField(max_length=255, null=True, blank=True, allow_unicode=True, editable=False,
                                  verbose_name='اسلاگ عنوان')

    def __str__(self):
        return self.title_fa

    class Meta:
        verbose_name = 'کلمه برجسته'
        verbose_name_plural = 'کلمات برجسته'


class AmazonProduct(models.Model):
    # general details
    asin = models.CharField(max_length=255, null=False, blank=True, unique=True, verbose_name='ASIN')
    amazon_product_root_domain = models.CharField(max_length=1000, null=True, blank=True,
                                                  verbose_name='لینک کشور-محصول آمازون')
    product_root_url = models.CharField(max_length=1000, null=True, blank=True,
                                        verbose_name='لینک ریشه محصول در آمازون')
    product_main_url = models.CharField(max_length=1000, null=True, blank=True,
                                        verbose_name='لینک اصلی محصول در آمازون')
    product_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='نوع محصول')

    # this field should be CharField
    title_fa = models.TextField(null=True, blank=True, verbose_name='عنوان فارسی')

    title_en = models.TextField(null=True, blank=True, verbose_name='عنوان انگلیسی')
    slug_title = models.SlugField(max_length=255, null=True, blank=True, editable=False, allow_unicode=True,
                                  verbose_name='اسلاگ عنوان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name='برند')
    categories = models.ManyToManyField(Category, related_name='product_categories', blank=True, verbose_name='دسته ها')
    keywords = models.ManyToManyField(Keyword, related_name='product_keywords', blank=True, verbose_name='کلمات برجسته')
    keywords_flat = models.TextField(null=True, blank=True, verbose_name='کلمات برجسته بصورت یکجا')
    product_brand_url = models.CharField(max_length=1000, null=True, blank=True,
                                         verbose_name='لینک برند محصول در آمازون')
    documents = models.ManyToManyField(Storage, related_name='product_documents', blank=True, verbose_name='مستندات')
    downloaded_documents = models.BooleanField(default=False, verbose_name='داکیومنت ها دانلود شده')
    variants = models.TextField(null=True, blank=True, verbose_name='variants')
    variants_asins_flat = models.TextField(null=True, blank=True, verbose_name='variants_asins_flat')
    has_size_guide = models.TextField(null=True, blank=True, verbose_name='has_size_guide')
    size_guide_html = models.TextField(null=True, blank=True, verbose_name='size_guide_html')
    user_rating_count = models.PositiveSmallIntegerField(null=True, blank=True,
                                                         verbose_name='تعداد امتیاز دهندگان به محصول')
    rating_score = models.FloatField(null=True, blank=True, verbose_name='امتیاز محصول')
    main_image = models.ImageField(upload_to='product-image/', null=True, blank=True, verbose_name='تصویر اصلی محصول')
    images = models.ManyToManyField(Storage, related_name='product_images', blank=True, verbose_name='تصاویر')
    downloaded_images = models.BooleanField(default=False, verbose_name='سایر تصاویر دانلود شده')
    feature_bullets = models.TextField(null=True, blank=True, verbose_name='ویژگی های کلیدی')
    attributes = models.TextField(null=True, blank=True, verbose_name='امکانات')
    weight = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='وزن بر اساس گرم')
    specifications = models.TextField(null=True, blank=True, verbose_name='مشخصات')

    # price
    currency = models.CharField(max_length=1000, null=True, blank=True, verbose_name='نماد ارز')
    base_price = models.FloatField(null=True, blank=True, verbose_name='قیمت پایه')
    discounted_price = models.FloatField(null=True, blank=True, verbose_name='قیمت تخفیف خورده')
    shipping_price = models.FloatField(null=True, blank=True, verbose_name='قیمت پایه حمل و نقل از آمازون')
    total_price = models.FloatField(null=True, blank=True, verbose_name='قیمت نهایی')
    discount_percentage = models.IntegerField(null=True, blank=True, verbose_name='درصد تخفیف')

    # website
    is_product_available = models.BooleanField(default=True, verbose_name='محصول فعال')
    is_product_special = models.BooleanField(default=False, verbose_name='محصول ویژه')

    # seo
    seo_title = models.TextField(null=True, blank=True, verbose_name='seo_title')
    seo_description = models.TextField(null=True, blank=True, verbose_name='seo_description')
    seo_keywords = models.TextField(null=True, blank=True, verbose_name='seo_keywords')
    slug = models.TextField(null=True, blank=True, verbose_name='slug')

    # admin
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amazon_product_created_by', null=False,
                                   blank=False, editable=False,
                                   verbose_name='کاربر ثبت کننده')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amazon_product_updated_by', null=False,
                                   blank=False, editable=False,
                                   verbose_name='کاربر بروز کننده')

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'محصول آمازون'
        verbose_name_plural = 'محصولات آمازون'

    def __str__(self):
        return self.asin

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)


class AddAmazonProduct(models.Model):
    asin = models.CharField(max_length=255, null=True, blank=True, verbose_name='asin')
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='link')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.link[:50]

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'افزودن محصول آمازون'
        verbose_name_plural = 'افزودن محصولات آمازون'


auditlog.register(AmazonProduct)
auditlog.register(AddAmazonProduct)
auditlog.register(Keyword)
auditlog.register(Category)

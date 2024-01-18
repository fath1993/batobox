import json
import threading
import time
from django.contrib import messages
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from amazon.models import AmazonProduct, Category, Keyword, AddAmazonProduct
from amazon.views import AmazonUpdateProductDetail
from custom_logs.models import custom_log


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title_fa',
        'title_en',
        'parent',
    )

    readonly_fields = (
        'title_slug',
        'parent_tree',
    )

    fields = (
        'parent',
        'title_fa',
        'title_en',
        'title_slug',
        'cat_image',

        'parent_tree',
    )

    @admin.action(description='بروز رسانی روابط')
    def update_parent_tree(self, request, queryset):
        AutoUpdateAllParentTree(queryset=queryset).start()

    actions = (update_parent_tree,)


class AutoUpdateAllParentTree(threading.Thread):
    def __init__(self, queryset):
        super().__init__()
        self.queryset = queryset

    def run(self):
        for category in self.queryset:
            parent_tree_list = []
            parent = category.parent
            if parent:
                if not parent.title_slug:
                    custom_title_slug = 'slug: null'
                else:
                    custom_title_slug = parent.title_slug
                if not parent.cat_image:
                    custom_cat_image_url = 'image: null'
                else:
                    custom_cat_image_url = parent.cat_image.url
                parent_tree_list.append([parent.id, parent.title_fa, parent.title_en, custom_title_slug, custom_cat_image_url])
                while True:
                    parent = parent.parent
                    if parent:
                        if not parent.title_slug:
                            custom_title_slug = 'slug: null'
                        else:
                            custom_title_slug = parent.title_slug
                        if not parent.cat_image:
                            custom_cat_image_url = 'image: null'
                        else:
                            custom_cat_image_url = parent.cat_image.url
                        parent_tree_list.append(
                            [parent.id, parent.title_fa, parent.title_en, custom_title_slug, custom_cat_image_url])
                    else:
                        break
            else:
                parent_tree_list.append('مادر است')
            category.parent_tree = json.dumps(parent_tree_list)
            category.save()


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = (
        'title_fa',
        'title_en',
    )

    readonly_fields = (
        'title_slug',
    )

    fields = (
        'title_fa',
        'title_en',
        'title_slug',
    )


@admin.register(AmazonProduct)
class AmazonProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'asin',
        'weight',
        'currency',
        'base_price',
        'discounted_price',
        'shipping_price',
        'total_price',
        'discount_percentage',
    )

    readonly_fields = (
        'slug_title',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    search_fields = (
        'asin',
        'created_by__username',
        'categories__title_fa',
        'categories__title_en',
    )

    fields = (
        'asin',
        'amazon_product_root_domain',
        'product_root_url',
        'product_main_url',
        'product_type',
        'title_fa',
        'title_en',
        'slug_title',
        'description',
        'brand',
        'product_brand_url',
        'documents',
        'downloaded_documents',
        'variants',
        'variants_asins_flat',
        'has_size_guide',
        'size_guide_html',
        'user_rating_count',
        'rating_score',
        'main_image',
        'images',
        'downloaded_images',
        'feature_bullets',
        'attributes',
        'weight',
        'specifications',
        'categories',
        'keywords',
        'keywords_flat',

        'currency',
        'base_price',
        'discounted_price',
        'shipping_price',
        'total_price',
        'discount_percentage',

        'is_product_available',
        'is_product_special',

        'seo_title',
        'seo_description',
        'seo_keywords',
        'slug',

        'created_at',
        'updated_at',
        'created_by',
        'updated_by',

    )

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
            instance.updated_by = request.user
        else:
            instance.updated_by = request.user

        instance.save()
        form.save_m2m()
        return instance

    @admin.action(description='دریافت اطلاعات جدید از rainforest api')
    def get_new_data_from_amazon_product_api(self, request, queryset):
        messages.info(request, f'عملیات در حال اجرا. زمان تقریبی تکمیل {queryset.count() * 10} ثانیه. تکمیل دریافت تصاویر در حدود {queryset.count()} دقیقه')
        AmazonUpdateProductDetail(request=request, amazon_products=queryset).start()
    actions = ('get_new_data_from_amazon_product_api', )


@admin.register(AddAmazonProduct)
class AddAmazonProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'link',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'asin',
        'link',
        'created_at',
    )

    @admin.action(description='ایجاد یا بروز رسانی محصولات')
    def get_or_create_product(self, request, queryset):
        amazon_product_list = []
        for product in queryset:
            amazon_asin = None
            if not product.asin:
                if str(product.link).find('https://www.amazon.ae/') != -1:
                    if str(product.link).find('/dp/') != -1:
                        start_index = str(product.link).find('/dp/') + 4
                        end_index = start_index + 10
                        amazon_asin = str(product.link)[start_index:end_index]
            else:
                amazon_asin = product.asin
            if amazon_asin:
                amazon_product = AmazonProduct.objects.get_or_create(asin=amazon_asin, created_by=request.user, updated_by=request.user)
                amazon_product_list.append(amazon_product[0])
            custom_log(f'amazon_asin: {amazon_asin}')
        for product in queryset:
            product.delete()
        messages.info(request,
                      f'عملیات در حال اجرا. زمان تقریبی تکمیل {len(amazon_product_list) * 10} ثانیه. تکمیل دریافت تصاویر در حدود {queryset.count()} دقیقه')
        AmazonUpdateProductDetail(request=request, amazon_products=amazon_product_list).start()

    actions = (get_or_create_product,)

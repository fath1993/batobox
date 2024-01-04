import json
import threading
import time
from django.contrib import messages
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from amazon.models import AmazonProduct, Category, Keyword
from amazon.views import AmazonUpdateProductDetail


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'parent',
        'title_fa',
        'title_en',
    )

    readonly_fields = (
        'title_slug',
        'parent_tree',
        'children',
    )

    fields = (
        'parent',
        'title_fa',
        'title_en',
        'title_slug',
        'cat_image',

        'children',
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
            category.children.clear()
            category.save()
        for category in self.queryset:
            parent_tree_list = []
            parent = category.parent
            if parent:
                parent.children.add(category)
                parent.save()
                if not parent.title_slug:
                    custom_title_slug = 'slug: null'
                else:
                    custom_title_slug = parent.title_slug
                if not parent.cat_image:
                    custom_cat_image_url = 'image: null'
                else:
                    custom_cat_image_url = parent.cat_image.url
                parent_tree_list.append([parent.title_fa, parent.title_en, custom_title_slug, custom_cat_image_url])
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
                            [parent.title_fa, parent.title_en, custom_title_slug, custom_cat_image_url])
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
    #     if not change:
    #         amazon_asin = None
    #         if not instance.asin:
    #             if instance.product_root_url:
    #                 if str(instance.product_root_url).find('https://www.amazon.ae/') != -1:
    #                     product_link = instance.product_root_url.split('/')
    #                     for section in product_link:
    #                         if len(section) == 10:
    #                             amazon_asin = section
    #             if not instance.product_root_url and instance.product_main_url:
    #                 if str(instance.product_main_url).find('https://www.amazon.ae/') != -1:
    #                     product_link = instance.product_main_url.split('/')
    #                     for section in product_link:
    #                         if len(section) == 10:
    #                             amazon_asin = section
    #         if amazon_asin:
    #             try:
    #                 old_amazon_product = AmazonProduct.objects.get(asin=amazon_asin)
    #                 self.message_user(request, f"محصول با asin {amazon_asin} از قبل موجود است", level='ERROR')
    #                 form._save_related_allowed = False
    #                 request.session['save_related_allowed'] = {'save_related_allowed': False}
    #                 return
    #             except:
    #                 instance.asin = amazon_asin
    #                 instance.save()
    #                 form.save_m2m()
    #                 request.session['save_related_allowed'] = {'save_related_allowed': True}
    #                 return instance
    #     else:
    #         instance.save()
    #         form.save_m2m()
    #         request.session['save_related_allowed'] = {'save_related_allowed': True}
    #         return instance
    #
    # def save_related(self, request, form, formsets, change):
    #     save_model_data = request.session.pop('save_related_allowed')
    #     if save_model_data['save_related_allowed']:
    #         super().save_related(request, form, formsets, change)


    @admin.action(description='دریافت اطلاعات جدید از rainforest api')
    def get_new_data_from_amazon_product_api(self, request, queryset):
        messages.info(request, f'عملیات در حال اجرا. زمان تقریبی تکمیل {queryset.count() * 10} ثانیه. تکمیل دریافت تصاویر در حدود {queryset.count()} دقیقه')
        AmazonUpdateProductDetail(request=request, amazon_products=queryset).start()
    actions = ('get_new_data_from_amazon_product_api', )

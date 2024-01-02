from django.contrib import admin

from website.models import BannerTopHeader, BannerTopFooter, BannerMiddleFooter, HomePageSlider, WhyUsReason, \
    FrequentlyAskedQuestion, TermAndCondition, PageSeo, Website, DynamicData, Brand


@admin.register(BannerTopHeader)
class BannerTopHeaderAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    fields = (
        'title',
        'link',
        'link_text',
        'image',
        'title_color',
        'btn_text_color',
        'btn_color',
    )


@admin.register(BannerTopFooter)
class BannerTopFooterAdmin(admin.ModelAdmin):
    list_display = (
        'link',
        'image',
    )

    fields = (
        'link',
        'image',
    )


@admin.register(BannerMiddleFooter)
class BannerMiddleFooterAdmin(admin.ModelAdmin):
    list_display = (
        'link',
        'image',
    )

    fields = (
        'link',
        'image',
    )


@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'sub_title',
    )

    fields = (
        'title',
        'sub_title',
        'description',
        'link',
        'link_text',
        'image_desktop',
        'image_tablet',
        'image_mobile',
    )


@admin.register(WhyUsReason)
class WhyUsReasonAdmin(admin.ModelAdmin):
    list_display = (
        'reason',
        'description',
    )

    fields = (
        'reason',
        'description',
        'image',
    )


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
    )

    fields = (
        'question',
        'answer',
    )


@admin.register(TermAndCondition)
class TermAndConditionAdmin(admin.ModelAdmin):
    list_display = (
        'law',
        'law_description',
    )

    fields = (
        'law',
        'law_description',
    )


@admin.register(PageSeo)
class PageSeoAdmin(admin.ModelAdmin):
    list_display = (
        'page',
        'title',
        'keywords',
        'description',
        'canonical',
        'robots',
        'page_type',
    )

    fields = (
        'page',
        'title',
        'keywords',
        'description',
        'canonical',
        'robots',
        'page_type',
        'image',
    )


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = (
        'site_type',
        'title',
        'description',
    )

    fields = (
        'site_type',
        'title',
        'description',
        'image',
        'link',
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'title_fa',
        'title_en',
        'title_slug',
        'description',
    )

    readonly_fields = (
        'title_slug',
    )

    fields = (
        'title_fa',
        'title_en',
        'title_slug',
        'description',
        'image',
        'link',
    )


@admin.register(DynamicData)
class DynamicDataAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )

    fields = (
        'key',
        'value',
    )
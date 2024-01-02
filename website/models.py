from django.db import models
from django.utils.text import slugify

COLOR_STYLE = (('light', 'light'), ('dark', 'dark'))
PAGES = (('صفحه اصلی', 'صفحه اصلی'), ('تماس با ما', 'تماس با ما'), ('درباره ما', 'درباره ما'),
         ('سوالات متداول', 'سوالات متداول'), ('سبد خرید', 'سبد خرید'),('پرداخت', 'پرداخت'),
         ('ماشین حساب امارات', 'ماشین حساب امارات'), ('ماشین حساب ترکیه', 'ماشین حساب ترکیه'),
         ('قوانین ما', 'قوانین ما'),)
ROBOTS = (('index, follow', 'index, follow'), ('noindex, nofollow', 'noindex, nofollow'), ('index', 'index'),
          ('follow', 'follow'), ('noindex', 'noindex'), ('nofollow', 'nofollow'),
          ('index, nofollow', 'index, nofollow'), ('noindex, follow', 'noindex, follow'),)
PAGE_TYPE = (('website', 'website'), ('article', 'article'), ('blog', 'blog'), ('book', 'book'),
             ('game', 'game'), ('film', 'film'), ('food', 'food'), ('city', 'city'), ('country', 'country'),
             ('actor', 'actor'), ('author', 'author'), ('politician', 'politician'), ('company', 'company'),
             ('hotel', 'hotel'), ('restaurant', 'restaurant'),)
WEBSITE_TYPE = (('turkey', 'ترکیه'), ('emirates', 'امارات'))


class BannerTopHeader(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    link = models.CharField(max_length=1000, null=True, blank=True, verbose_name='لینک')
    link_text = models.CharField(max_length=255, null=False, blank=False, verbose_name='متن لینک')
    image = models.ImageField(upload_to='website/banner-top-header/', null=False, blank=False, verbose_name='تصویر')

    title_color = models.CharField(max_length=255, default='light', null=False, blank=False, choices=COLOR_STYLE,
                                   verbose_name='نوع رنگبندی عنوان')
    btn_text_color = models.CharField(max_length=255, default='light', null=False, blank=False, choices=COLOR_STYLE,
                                      verbose_name='نوع رنگبندی متن دکمه')
    btn_color = models.CharField(max_length=255, default='light', null=False, blank=False, choices=COLOR_STYLE,
                                 verbose_name='نوع رنگبندی دکمه')

    class Meta:
        verbose_name = 'بنر بالای هدر'
        verbose_name_plural = 'بنر های بالای هدر'


class BannerTopFooter(models.Model):
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='لینک')
    image = models.ImageField(upload_to='website/banner-top-footer/', null=False, blank=False, verbose_name='تصویر')

    class Meta:
        verbose_name = 'بنر بالای فوتر'
        verbose_name_plural = 'بنر های بالای فوتر'


class BannerMiddleFooter(models.Model):
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='لینک')
    image = models.ImageField(upload_to='website/banner-middle-footer/', null=False, blank=False, verbose_name='تصویر')

    class Meta:
        verbose_name = 'بنر میانه صفحه'
        verbose_name_plural = 'بنر های میانه صفحه'


class HomePageSlider(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    sub_title = models.CharField(max_length=255, null=False, blank=False, verbose_name='زیر عنوان')
    description = models.CharField(max_length=255, null=False, blank=False, verbose_name='توضیحات')
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='لینک')
    link_text = models.CharField(max_length=255, null=False, blank=False, verbose_name='متن لینک')
    image_desktop = models.ImageField(upload_to='website/home-page-slider-desktop/', null=False, blank=False,
                                      verbose_name='تصویر دسکتاپ')
    image_tablet = models.ImageField(upload_to='website/home-page-slider-tablet/', null=False, blank=False,
                                     verbose_name='تصویر تبلت')
    image_mobile = models.ImageField(upload_to='website/home-page-slider-mobile/', null=False, blank=False,
                                     verbose_name='تصویر موبایل')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدر خانه'


class WhyUsReason(models.Model):
    reason = models.CharField(max_length=255, null=False, blank=False, verbose_name='دلیل')
    description = models.TextField(null=False, blank=False, verbose_name='توضیحات')
    image = models.ImageField(upload_to='website/why-us-reason/', null=False, blank=False)

    class Meta:
        verbose_name = 'دلیل خرید از ما'
        verbose_name_plural = 'دلایل خرید از ما'


class FrequentlyAskedQuestion(models.Model):
    question = models.CharField(max_length=255, null=False, blank=False, verbose_name='سوال')
    answer = models.TextField(null=False, blank=False, verbose_name='جواب')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات متداول'


class TermAndCondition(models.Model):
    law = models.CharField(max_length=255, null=False, blank=False, verbose_name='قانون')
    law_description = models.TextField(null=False, blank=False, verbose_name='توضیحات قانون')

    class Meta:
        verbose_name = 'شرط و قانون'
        verbose_name_plural = 'شرایط و قوانین'


class PageSeo(models.Model):
    page = models.CharField(max_length=255, choices=PAGES, null=False, blank=False, verbose_name='صفحه')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    keywords = models.CharField(max_length=255, null=False, blank=False, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, null=False, blank=False, verbose_name='توضیحات')
    canonical = models.CharField(max_length=1000, null=False, blank=False, verbose_name='کنونیکال')
    robots = models.CharField(max_length=255, choices=ROBOTS, null=False, blank=False, verbose_name='عملکرد ربات')
    page_type = models.CharField(max_length=255, choices=PAGE_TYPE, null=False, blank=False, verbose_name='نوع صفحه')
    image = models.ImageField(upload_to='website/page-seo-tool/', null=False, blank=False, verbose_name='تصویر صفحه')


    class Meta:
        verbose_name = "سئو صفحه"
        verbose_name_plural = "سئو صفحات"


class Website(models.Model):
    site_type = models.CharField(max_length=255, choices=WEBSITE_TYPE, null=False, blank=False, verbose_name='نوع سایت')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    description = models.CharField(max_length=1000, null=False, blank=False, verbose_name='توضیحات')
    image = models.ImageField(upload_to='website/', null=False, blank=False, verbose_name='تصویر')
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='لینک')

    class Meta:
        verbose_name = 'سایت'
        verbose_name_plural = 'سایت ها'


class Brand(models.Model):
    title_fa = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان فارسی')
    title_en = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان انگلیسی')
    title_slug = models.SlugField(max_length=255, null=True, blank=True, allow_unicode=True, editable=False,
                                  verbose_name='اسلاگ عنوان')
    description = models.CharField(max_length=1000, null=True, blank=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='website/', null=True, blank=True, verbose_name='تصویر')
    link = models.CharField(max_length=1000, null=True, blank=True, verbose_name='لینک')

    def __str__(self):
        return f'title_fa: {self.title_fa} | title_en: {self.title_en}'

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)


class DynamicData(models.Model):
    key = models.CharField(max_length=255, null=False, blank=False, verbose_name='کلید')
    value = models.TextField(null=False, blank=False, verbose_name='مقدار')

    def __str__(self):
        return f'key: {self.key} | value: {self.value[:20]}'

    class Meta:
        verbose_name = "داینامیک دیتا"
        verbose_name_plural = "داینامیک دیتا"

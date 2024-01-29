import uuid

from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel
from amazon.models import AmazonProduct
from storage.models import Storage
from auditlog.registry import auditlog


REQUEST_STATUS = (('در حال بررسی', 'در حال بررسی'), ('پرداخت شده و در انتظار بررسی', 'پرداخت شده و در انتظار بررسی'),
                ('در انتظار پرداخت مبلغ اصلاحیه', 'در انتظار پرداخت مبلغ اصلاحیه'), ('دریافت سفارش', 'دریافت سفارش'),
                ('ثبت سفارش در سایت خارجی', 'ثبت سفارش در سایت خارجی'), ('در واحد خارج از کشور', 'در واحد خارج از کشور'),
                ('ارسال به ایران', 'ارسال به ایران'), ('در گمرک', 'در گمرک'), ('در انبار باتوباکس', 'در انبار باتوباکس'),
                ('ارسال شده', 'ارسال شده'), ('تکمیل شده', 'تکمیل شده'), ('لغو شده', 'لغو شده'))


class Currency(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    badge = models.CharField(max_length=255, null=False, blank=False, verbose_name='نماد')
    currency_equivalent_price_in_toman = models.PositiveIntegerField(null=False, blank=False,
                                                                     verbose_name='قیمت پایه واحد ارز به تومان')
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    unique_code = models.CharField(max_length=255, null=False, blank=False, editable=False, verbose_name='کد یکتا')

    def __str__(self):
        return f'name: {self.name} | price: {self.currency_equivalent_price_in_toman}'

    class Meta:
        verbose_name = 'ارز'
        verbose_name_plural = 'ارز ها'

    def save(self, *args, **kwargs):
        self.unique_code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class BatoboxShipping(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, blank=False, verbose_name='هزینه حمل مرتبط به ارز با نماد')
    weight_from = models.PositiveIntegerField(null=False, blank=False, verbose_name='وزن از (واحد گرم)')
    weight_to = models.PositiveIntegerField(null=False, blank=False, verbose_name='وزن تا (واحد گرم)')
    price = models.PositiveIntegerField(null=False, blank=False, verbose_name='مبلغ به واحد ارز')
    unique_code = models.CharField(max_length=255, null=False, blank=False, editable=False,
                                   verbose_name='کد یکتا')

    def __str__(self):
        return f'name: {self.currency.badge} | weight: from {self.weight_from} to {self.weight_to} | price: {self.price}'

    class Meta:
        verbose_name = 'هزینه حمل و نقل باتوباکس'
        verbose_name_plural = 'هزینه های حمل و نقل باتوباکس'

    def save(self, *args, **kwargs):
        self.unique_code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class BatoboxCurrencyExchangeCommission(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, blank=False,
                                 verbose_name='کمیسون مرتبط به ارز با نماد')
    price_from = models.PositiveIntegerField(null=False, blank=False, verbose_name='قیمت از')
    price_to = models.PositiveIntegerField(null=False, blank=False, verbose_name='قیمت تا')
    exchange_percentage = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='درصد کارمزد تبدیل')
    unique_code = models.CharField(max_length=255, null=False, blank=False, editable=False,
                                   verbose_name='کد یکتا')

    def __str__(self):
        return f'name: {self.currency.badge} | price: from {self.price_from} to {self.price_to} | exchange_percentage: {self.exchange_percentage}'

    class Meta:
        verbose_name = 'کارمزد تبدیل ارز باتوباکس'
        verbose_name_plural = 'کارمزد های تبدیل ارز باتوباکس'


    def save(self, *args, **kwargs):
        self.unique_code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class RequestedProduct(models.Model):
    request_status = models.CharField(max_length=255, choices=REQUEST_STATUS, default='در حال بررسی', verbose_name='وضعیت سفارش')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='لینک')
    currency = models.TextField(null=True, blank=True, verbose_name='اطلاعات ارز')
    batobox_shipping = models.TextField(null=True, blank=True, verbose_name='اطلاعات حمل و نقل')
    batobox_currency_exchange_commission = models.TextField(null=True, blank=True, verbose_name='اطلاعات کمیسیون')
    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name='وزن به گرم')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات کاربر')
    numbers = models.PositiveSmallIntegerField(default=0, null=True, blank=True, verbose_name='تعداد')

    product_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت محصول به واحد ارز')
    batobox_shipping_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت حمل و نقل به واحد ارز')
    final_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت نهایی به واحد ارز')
    currency_equivalent_price_in_toman = models.PositiveIntegerField(null=True, blank=True,
                                                                     verbose_name='قیمت واحد ارز به تومان')
    currency_exchange_percentage = models.PositiveIntegerField(null=True, blank=True,
                                                               verbose_name='درصد کمیسیون تبدیل ارز')
    final_price_in_toman_single = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت نهایی تک محصول به تومان')
    final_price_in_toman_multiple = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت نهایی محصول با احتساب تعداد به تومان')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_by', null=False,
                                   blank=False, editable=False,
                                   verbose_name='کاربر ثبت کننده')

    class Meta:
        verbose_name = 'درخواست محصول'
        verbose_name_plural = 'درخواست های محصولات'

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if not self.request_status:
            self.request_status = 'در حال بررسی'
        super().save(*args, **kwargs)


class ProductCalculatorAccessHistory(models.Model):
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, editable=False,
                                   verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'{self.created_by.username} | {self.created_at.strftime("%Y/%m/%d")}'

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'سابقه دسترسی به محاسبه گر محصولات'
        verbose_name_plural = 'سوابق دسترسی به محاسبه گر محصولات'


class RainForestApiAccessHistory(models.Model):
    api_query_result = models.TextField(max_length=255, null=False, blank=False, editable=False, verbose_name='نتیجه درخواست')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, editable=False,
                                   verbose_name='ایجاد شده توسط')

    def __str__(self):
        return f'{self.created_by.username} | {self.created_at.strftime("%Y/%m/%d")}'

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'سابقه دسترسی به rainforest api'
        verbose_name_plural = 'سوابق دسترسی به rainforest api'


auditlog.register(Currency)
auditlog.register(BatoboxShipping)
auditlog.register(BatoboxCurrencyExchangeCommission)
auditlog.register(RequestedProduct)
auditlog.register(ProductCalculatorAccessHistory)
auditlog.register(RainForestApiAccessHistory)
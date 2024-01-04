import jdatetime
from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from store.models import RequestedProduct

ORDER_STATUS = (('در حال بررسی', 'در حال بررسی'), ('پرداخت شده و در انتظار بررسی', 'پرداخت شده و در انتظار بررسی'), ('در انتظار پرداخت مبلغ اصلاحیه', 'در انتظار پرداخت مبلغ اصلاحیه'),
                ('درحال آماده سازی', 'درحال آماده سازی'), ('ارسال شده', 'ارسال شده'),
                ('لغو شده', 'لغو شده'), ('ارسال به ایران', 'ارسال به ایران'), ('در گمرک', 'در گمرک'), ('در انبار باتوباکس', 'در انبار باتوباکس'), ('تکمیل شده', 'تکمیل شده'))

TRANSACTION_STATUS = (('پرداخت نشده', 'پرداخت نشده'), ('پرداخت شده', 'پرداخت شده'))


class SMSAuthCode(models.Model):
    phone_number = models.CharField(max_length=255, null=False, blank=False, editable=False,
                                    verbose_name='شماره موبایل')
    pass_code = models.CharField(max_length=255, null=False, blank=False, editable=False, verbose_name='کد احراز')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'کد تایید پیامکی'
        verbose_name_plural = 'کد های تایید پیامکی'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, null=False, blank=False,
                                editable=False, verbose_name='کاربر')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام خانوادگی')
    landline = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره ثابت')
    birthday = jmodel.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    province = models.CharField(max_length=255, null=True, blank=True, verbose_name='استان')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name='شهر')
    zip_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='کد پستی')
    wallet_balance = models.PositiveIntegerField(default=0, verbose_name='اعتبار کیف پول')

    # based on json
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    like_list = models.TextField(null=True, blank=True, verbose_name='لیست محصولات مورد علاقه')
    wish_list = models.TextField(null=True, blank=True, verbose_name='لیست خرید های احتمالی در آینده')
    temp_card = models.TextField(null=True, blank=True, verbose_name='محصولات در سبد خرید')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class PaymentCode(models.Model):
    user = models.ForeignKey(User, related_name='user_wallet_change_code', on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    unique_code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد یکتا')
    is_used = models.BooleanField(default=False, verbose_name='استفاده شده')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'کد پرداخت'
        verbose_name_plural = 'کد های پرداخت'


class Order(models.Model):
    products = models.ManyToManyField(RequestedProduct, blank=True, verbose_name='محصولات نهایی شده')
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='در حال بررسی', verbose_name='وضعیت سفارش')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحات')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='order_user_created_by', editable=False, verbose_name='کاربر')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='order_user_updated_by', editable=False, verbose_name='کاربر')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False, verbose_name='سفارش')

    amount = models.PositiveIntegerField(null=False, blank=False, verbose_name='مبلغ - تومان')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحات')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='ایمیل')
    mobile = models.CharField(max_length=255, null=True, blank=True, verbose_name='موبایل')


    authority = models.CharField(max_length=255, null=True, blank=True)
    ref_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=TRANSACTION_STATUS, default='pending', null=False,
                              blank=False, verbose_name='وضعیت')

    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')

    def __str__(self):
        return f'order: {self.order.id} | amount: {self.amount}'

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'


auditlog.register(SMSAuthCode)
auditlog.register(Profile)
auditlog.register(Order)
auditlog.register(Transaction)

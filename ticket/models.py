from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel

from storage.models import Storage

TICKET_STATUS = (('ایجاد شده', 'ایجاد شده'), ('در حال بررسی', 'در حال بررسی'), ('پاسخ ادمین', 'پاسخ ادمین'),
                 ('بسته شده', 'بسته شده'), ('پاسخ کاربر', 'پاسخ کاربر'), )


class Ticket(models.Model):
    status = models.CharField(max_length=255, choices=TICKET_STATUS, default='pending', null=False, blank=False,
                              verbose_name='وضعیت تیکت')
    title = models.CharField(max_length=512, null=True, blank=True, verbose_name='عنوان تیکت')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    created_by = models.ForeignKey(User, related_name='ticket_created_by', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=True, verbose_name='متعلق به')
    updated_by = models.ForeignKey(User, related_name='ticket_updated_by', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='بروز شده توسط')

    def __str__(self):
        return f'{self.created_by.username} | {self.title[:20]}'

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='ticket_message', on_delete=models.CASCADE, null=False, blank=False,
                               verbose_name='تیکت')
    content = models.TextField(null=False, blank=False, verbose_name='محتوا')
    attachments = models.ManyToManyField(Storage, blank=True, verbose_name='ضمائم')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(User, related_name='created_by_message', on_delete=models.CASCADE, null=False,
                                   blank=False, editable=False, verbose_name='ساخته شده توسط')

    def __str__(self):
        return f'{self.ticket.title[:20]} | {self.content[:20]}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


    def save(self, *args, **kwargs):
        self.ticket.updated_by = self.created_by
        if self.created_by.is_superuser or self.created_by.is_staff:
            self.ticket.status = 'پاسخ ادمین'
        else:
            self.ticket.status = 'پاسخ کاربر'
        self.ticket.save()
        super().save(*args, **kwargs)

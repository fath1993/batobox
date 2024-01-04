from django.contrib import admin
from accounts.models import Profile, SMSAuthCode, Order, Transaction, PaymentCode


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'wallet_balance',
    )

    readonly_fields = (
        'user',
    )

    fields = (
        'user',
        'first_name',
        'last_name',
        'landline',
        'birthday',
        'province',
        'city',
        'zip_code',
        'wallet_balance',
        'address',
        'like_list',
        'wish_list',
        'temp_card',
    )

    def has_add_permission(self, request):
        return False


@admin.register(PaymentCode)
class PaymentCodeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'unique_code',
        'is_used',
    )

    fields = (
        'user',
        'unique_code',
        'is_used',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'display_id_display',
        'order_status',
        'description',
        'created_at_display',
        'updated_at_display',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'products',
        'order_status',
        'description',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    @admin.display(description="شماره سفارش", empty_value='???')
    def display_id_display(self, obj):
        display_id = obj.id
        return display_id

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        data_time = str(obj.created_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
            instance.updated_by = request.user
        else:
            instance.updated_by = request.user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'amount',
        'description',
        'status',
        'created_at_display',
        'updated_at_display',
    )

    search_fields = (
        'order__id',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'order',
        'amount',
        'description',
        'email',
        'mobile',

        'authority',
        'ref_id',
        'status',

        'created_at',
        'updated_at',
    )

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        data_time = str(obj.created_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

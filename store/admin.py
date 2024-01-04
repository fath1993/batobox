from django.contrib import admin
from store.models import Currency, RequestedProduct, ProductCalculatorAccessHistory, \
    RainForestApiAccessHistory, BatoboxShipping, BatoboxCurrencyExchangeCommission


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'badge',
        'currency_equivalent_price_in_toman',
        'is_active',
    )

    readonly_fields = (
        'unique_code',
    )

    fields = (
        'name',
        'badge',
        'currency_equivalent_price_in_toman',
        'is_active',
        'unique_code',
    )


@admin.register(BatoboxShipping)
class BatoboxShippingAdmin(admin.ModelAdmin):
    list_display = (
        'currency',
        'weight_from',
        'weight_to',
        'price',
    )

    readonly_fields = (
        'unique_code',
    )

    fields = (
        'currency',
        'weight_from',
        'weight_to',
        'price',
        'unique_code',
    )


@admin.register(BatoboxCurrencyExchangeCommission)
class BatoboxCurrencyExchangeCommissionAdmin(admin.ModelAdmin):
    list_display = (
        'currency',
        'price_from',
        'price_to',
        'exchange_percentage',
    )

    readonly_fields = (
        'unique_code',
    )

    fields = (
        'currency',
        'price_from',
        'price_to',
        'exchange_percentage',
        'unique_code',
    )


@admin.register(RequestedProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'link',
        'description',
        'final_price',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
        'link',
        'currency',
        'batobox_shipping',
        'batobox_currency_exchange_commission',
        'weight',
        'description',
        'numbers',
        'product_price',
        'batobox_shipping_price',
        'final_price',
        'currency_equivalent_price_in_toman',
        'currency_exchange_percentage',
        'final_price_in_toman',
        'created_at',
        'created_by',
    )

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(ProductCalculatorAccessHistory)
class ProductCalculatorAccessHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'created_by',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
        'created_at',
        'created_by',
    )

    def has_add_permission(self, request):
        return False


@admin.register(RainForestApiAccessHistory)
class RainForestApiAccessHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'api_query_result',
        'created_at',
        'created_by',
    )

    readonly_fields = (
        'api_query_result',
        'created_at',
        'created_by',
    )

    fields = (
        'api_query_result',
        'created_at',
        'created_by',
    )

    def has_add_permission(self, request):
        return False

from django.urls import path, include
from store.views import ProductPriceCalculator, ProductView, ProductListView, CurrencyListView, OrderView, \
    BatoboxShippingListView, BatoboxCurrencyExchangeCommissionListView, RequestPayView, PayConfirmView, OrderListView, \
    TransactionListView, CategoryListView, UpdateRequestedProductsView

app_name = 'store'

urlpatterns = (
    # product
    path('api/product-price-calculator/', ProductPriceCalculator.as_view(), name='product-price-calculator'),
    path('api/product/', ProductView.as_view(), name='product'),
    path('api/product-list/', ProductListView.as_view(), name='product-list'),
    path('api/categories/', CategoryListView.as_view(), name='categories'),

    # store
    path('api/update-request-products/', UpdateRequestedProductsView.as_view(), name='update-request-products'),
    path('api/order/', OrderView.as_view(), name='order'),
    path('api/request-pay/', RequestPayView.as_view(), name='request-pay'),
    path('api/pay-confirm/', PayConfirmView.as_view(), name='pay-confirm'),
    path('api/order-list/', OrderListView.as_view(), name='order-list'),
    path('api/transaction-list/', TransactionListView.as_view(), name='transaction-list'),

    # commissions
    path('api/currency-list/', CurrencyListView.as_view(), name='currency-list'),
    path('api/batobox-shipping-list/', BatoboxShippingListView.as_view(), name='batobox-shipping-list'),
    path('api/batobox-currency-exchange-commission-list/', BatoboxCurrencyExchangeCommissionListView.as_view(), name='batobox-currency-exchange-commission-list'),

)




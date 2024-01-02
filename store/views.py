import json
import uuid

import jdatetime
import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from accounts.models import Order, Transaction, PaymentCode
from accounts.serializer import OrderSerializer, TransactionSerializer
from amazon.models import AmazonProduct, Category, Keyword
from amazon.serializer import AmazonProductSerializer, CategorySerializer, KeywordSerializer
from amazon.views import update_amazon_product_from_rainforest_api
from batobox.settings import ZARINPAL_API_KEY, BASE_URL, BASE_FRONT_URL
from custom_logs.models import custom_log
from store.models import ProductCalculatorAccessHistory, RequestedProduct, Currency, BatoboxShipping, \
    BatoboxCurrencyExchangeCommission
from store.serializer import CurrencySerializer, BatoboxShippingSerializer, BatoboxCurrencyExchangeCommissionSerializer
from utilities.http_metod import fetch_data_from_http_get
from utilities.utilities import create_json, date_string_to_date_format


class ProductPriceCalculator(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        default_provided_url = None
        batobox_product_url = None
        batobox_product_id = None
        currency = None
        weight = None
        price = None
        now = jdatetime.datetime.now()
        try:
            all_product_calculator_access_history = ProductCalculatorAccessHistory.objects.filter(
                created_by=request.user)
            if all_product_calculator_access_history.count() != 0:
                latest_product_calculator_access_history = all_product_calculator_access_history.latest('created_at')
                total_seconds_between_request = (
                        now - latest_product_calculator_access_history.created_at).total_seconds()
                if total_seconds_between_request < 1:
                    return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                    f'درخواست مجدد پس از گذشت {int(round(200 - total_seconds_between_request, 0))} ثانیه امکان پذیر است.'))
        except Exception as e:
            pass
        ProductCalculatorAccessHistory.objects.create(created_by=request.user)
        try:
            front_input = json.loads(request.body)
            try:
                product_link = front_input['product_link']
                if product_link == '':
                    product_link = None
            except:
                product_link = None
            try:
                amazon_asin = front_input['amazon_asin']
                if amazon_asin == '':
                    amazon_asin = None
            except:
                amazon_asin = None
            try:
                currency_unique_code = front_input['currency_unique_code']
                if currency_unique_code == '':
                    currency_unique_code = None
            except:
                currency_unique_code = None
            if not currency_unique_code:
                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                f'ارسال پارامتر currency_unique_code ضروری است'))
            else:
                try:
                    currency = Currency.objects.get(unique_code=currency_unique_code)
                except:
                    return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                    f'پارامتر currency_unique_code صحیح نیست یا منقضی شده است'))
            try:
                batobox_shipping_unique_code = front_input['batobox_shipping_unique_code']
                if batobox_shipping_unique_code == '':
                    batobox_shipping_unique_code = None
            except:
                batobox_shipping_unique_code = None
            if not batobox_shipping_unique_code:
                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                f'ارسال پارامتر batobox_shipping_unique_code ضروری است'))
            else:
                try:
                    batobox_shipping = BatoboxShipping.objects.get(unique_code=batobox_shipping_unique_code)
                except:
                    return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                    f'پارامتر batobox_shipping_unique_code صحیح نیست یا منقضی شده است'))
            try:
                batobox_currency_exchange_unique_code = front_input['batobox_currency_exchange_unique_code']
                if batobox_currency_exchange_unique_code == '':
                    batobox_currency_exchange_unique_code = None
            except:
                batobox_currency_exchange_unique_code = None
            if not batobox_currency_exchange_unique_code:
                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                f'ارسال پارامتر batobox_currency_exchange_unique_code ضروری است'))
            else:
                try:
                    batobox_currency_exchange_commission = BatoboxCurrencyExchangeCommission.objects.get(
                        unique_code=batobox_currency_exchange_unique_code)
                except:
                    return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                    f'پارامتر batobox_currency_exchange_unique_code صحیح نیست یا منقضی شده است'))
            if product_link is None and amazon_asin is None:
                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                f'ارسال یکی از پارامتر های amazon_asin یا product_link ضروری است'))
            if product_link is not None and amazon_asin is not None:
                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                f'ارسال تنها یکی از پارامتر های amazon_asin یا product_link مجاز است'))
            try:
                weight = front_input['weight']
                if weight == '':
                    weight = None
                if weight is not None:
                    try:
                        weight = int(weight)
                    except:
                        weight = None
            except:
                weight = None
            try:
                price = front_input['price']
                if price == '':
                    price = None
                if price is not None:
                    try:
                        price = float(price)
                    except:
                        price = None
            except:
                price = None
            try:
                description = front_input['description']
                if description == '':
                    description = None
            except:
                description = None

            if product_link:
                default_provided_url = product_link
                if str(product_link).find('https://www.amazon.ae/') != -1:
                    product_link = product_link.split('/')
                    for section in product_link:
                        if len(section) == 10:
                            amazon_asin = section
                else:
                    if not currency:
                        return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                        f'ارسال نماد ارز برای محصولات غیر از آمازون ضروری است'))
                    if not weight:
                        return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                        f'ارسال وزن برای محصولات غیر از آمازون ضروری است'))
                    if not price:
                        return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                        f'ارسال قیمت برای محصولات غیر از آمازون ضروری است'))
            if amazon_asin:
                try:
                    amazon_product = AmazonProduct.objects.get(asin=amazon_asin)
                    batobox_product_id = amazon_product.id
                    if not amazon_product.currency or not amazon_product.weight or not amazon_product.total_price:
                        update_product_from_api = True
                    elif amazon_product.weight == 0:
                        update_product_from_api = True
                    elif (now - amazon_product.updated_at).total_seconds() > (15 * 60):
                        update_product_from_api = True
                    else:
                        update_product_from_api = False
                        weight = amazon_product.weight
                        price = amazon_product.total_price
                        default_provided_url = amazon_product.product_main_url
                except Exception as e:
                    amazon_product = AmazonProduct.objects.create(
                        asin=amazon_asin,
                        created_by=request.user,
                        updated_by=request.user,
                    )
                    batobox_product_id = amazon_product.id
                    update_product_from_api = True
                if update_product_from_api:
                    default_provided_url = f'amazon asin: {amazon_asin}'
                    amazon_product_new_data_from_api = update_amazon_product_from_rainforest_api(amazon_product)
                    response_data_from_amazon_api = json.loads(amazon_product_new_data_from_api.content)
                    custom_log(response_data_from_amazon_api)
                    try:
                        request_info_success = response_data_from_amazon_api['request_info_success']
                        if request_info_success == 'false':
                            batobox_product_id = None
                            if not currency:
                                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                                f'ارتباط بر خط برای دریافت اطلاعات محصول ممکن نیست. ارسال نماد ارز برای محاسبه قیمت ضروری است'))
                            if not weight:
                                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                                f'ارتباط بر خط برای دریافت اطلاعات محصول ممکن نیست. ارسال وزن برای محاسبه قیمت ضروری است'))
                            if not price:
                                return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                                f'ارتباط بر خط برای دریافت اطلاعات محصول ممکن نیست. ارسال قیمت برای محاسبه قیمت نهایی ضروری است'))
                        else:
                            currency = response_data_from_amazon_api['currency']
                            weight = response_data_from_amazon_api['weight']
                            price = response_data_from_amazon_api['total_price']
                            default_provided_url = response_data_from_amazon_api['product_main_url']
                    except Exception as e:
                        custom_log(str(e))
                        batobox_product_id = None
                        if not currency:
                            return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                            f'محصول آمازون یافت نشد. ارسال نماد ارز برای محاسبه قیمت ضروری است'))
                        if not weight:
                            return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                            f'محصول آمازون یافت نشد. ارسال وزن برای محاسبه قیمت ضروری است'))
                        if not price:
                            return JsonResponse(create_json('post', 'محاسبه قیمت', 'ناموفق',
                                                            f'محصول آمازون یافت نشد. ارسال قیمت برای محاسبه قیمت نهایی ضروری است'))
            currency_json = {
                'name': currency.name,
                'badge': currency.badge,
                'currency_equivalent_price_in_toman': currency.currency_equivalent_price_in_toman,
                'is_active': currency.is_active,
                'unique_code': currency.unique_code,
            }
            batobox_shipping_json = {
                'currency': currency.badge,
                'weight_from': batobox_shipping.weight_from,
                'weight_to': batobox_shipping.weight_to,
                'price': batobox_shipping.price,
                'unique_code': batobox_shipping.unique_code,
            }
            batobox_currency_exchange_commission_json = {
                'currency': currency.badge,
                'price_from': batobox_currency_exchange_commission.price_from,
                'price_to': batobox_currency_exchange_commission.price_to,
                'exchange_percentage': batobox_currency_exchange_commission.exchange_percentage,
                'unique_code': batobox_currency_exchange_commission.unique_code,
            }
            product_price = price
            batobox_shipping_price = batobox_shipping.price
            final_price = product_price + batobox_shipping_price
            currency_exchange_percentage = batobox_currency_exchange_commission.exchange_percentage
            currency_equivalent_price_in_toman = currency.currency_equivalent_price_in_toman
            final_price_in_toman = (price + batobox_shipping_price) * float(currency_equivalent_price_in_toman) * float(f'1.{currency_exchange_percentage}')
            final_price_in_toman = int(round(final_price_in_toman, -3))
            new_requested_product = RequestedProduct.objects.create(
                link=default_provided_url,
                currency=json.dumps(currency_json),
                batobox_shipping=json.dumps(batobox_shipping_json),
                batobox_currency_exchange_commission=json.dumps(batobox_currency_exchange_commission_json),
                weight=weight,
                description=description,
                product_price=product_price,
                batobox_shipping_price=batobox_shipping_price,
                final_price=final_price,
                currency_equivalent_price_in_toman=currency_equivalent_price_in_toman,
                currency_exchange_percentage=currency_exchange_percentage,
                final_price_in_toman=final_price_in_toman,
                created_at=request.user,
                created_by=request.user,
            )

            json_response_body = {
                'method': 'post',
                'request': 'محاسبه قیمت',
                'result': 'موفق',
                'product_detail': {
                    'requested_product_id': new_requested_product.id,
                    'link': default_provided_url,
                    'currency': currency_json,
                    'batobox_shipping': batobox_shipping_json,
                    'batobox_currency_exchange_commission': batobox_currency_exchange_commission_json,
                    'weight': weight,
                    'description': description,
                    'product_price': product_price,
                    'batobox_shipping_price': batobox_shipping_price,
                    'final_price': final_price,
                    'currency_equivalent_price_in_toman': currency_equivalent_price_in_toman,
                    'currency_exchange_percentage': currency_exchange_percentage,
                    'final_price_in_toman': final_price_in_toman,
                }
            }
            if batobox_product_id:
                json_response_body['batobox_product_id'] = batobox_product_id
            return JsonResponse(json_response_body)
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'محصول جدید', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class ProductView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                product_id = front_input['product_id']
                amazon_product_asin = front_input['amazon_product_asin']
                if product_id is None:
                    print('آیدی محصول خالی است')
                    return JsonResponse(create_json('post', 'جزئیات محصول آمازون', 'ناموفق', f'آیدی محصول خالی است'))
                if amazon_product_asin is None:
                    print('شناسه محصول آمازون خالی است')
                    return JsonResponse(
                        create_json('post', 'جزئیات محصول آمازون', 'ناموفق', f'شناسه محصول آمازون خالی است'))
                try:
                    amazon_product = AmazonProduct.objects.filter(id=product_id, asin=amazon_product_asin)
                    if amazon_product.count() == 0:
                        raise Exception
                    serializer = AmazonProductSerializer(amazon_product, many=True)
                    return Response(serializer.data)
                except Exception as e:
                    print(str(e))
                    return JsonResponse(create_json('post', 'جزئیات محصول آمازون', 'ناموفق',
                                                    f'اطلاعات محصول آمازون با آیدی {product_id} و شناسه {amazon_product_asin} یافت نشد.'))
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'جزئیات محصول آمازون', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'جزئیات محصول آمازون', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class ProductListView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            product_label = front_input['product_label']
            if product_label != 'amazon':
                return JsonResponse(create_json('post', 'فیلتر محصولات آمازون', 'ناموفق',
                                                f'در حال حاضر تنها محصولات آمازون بتوباکس پشتیبانی می شود'))
            try:
                try:
                    date_range_from = front_input['date_range_from']
                    if date_range_from == '':
                        raise
                    date_range_from = date_string_to_date_format(date_range_from)
                except:
                    date_range_from = None
                try:
                    date_range_to = front_input['date_range_to']
                    if date_range_to == '':
                        raise
                    date_range_to = date_string_to_date_format(date_range_to)
                except:
                    date_range_to = None
                try:
                    price_range_from = front_input['price_range_from']
                    if price_range_from == '':
                        raise
                    try:
                        price_range_from = int(price_range_from)
                    except:
                        price_range_from = None
                except:
                    price_range_from = None
                try:
                    price_range_to = front_input['price_range_to']
                    if price_range_to == '':
                        raise
                    try:
                        price_range_to = int(price_range_to)
                    except:
                        price_range_to = None
                except:
                    price_range_to = None
                try:
                    score_range_from = front_input['score_range_from']
                    if score_range_from == '':
                        raise
                    try:
                        price_range_to = float(score_range_from)
                    except:
                        score_range_from = None
                except:
                    score_range_from = None
                try:
                    score_range_to = front_input['score_range_to']
                    if score_range_to == '':
                        raise
                    try:
                        score_range_to = float(score_range_to)
                    except:
                        score_range_to = None
                except:
                    score_range_to = None
                try:
                    category_words_list = front_input['category_words_list']
                    if category_words_list == '':
                        raise
                    try:
                        category_words_list = str(category_words_list).split(',')
                    except:
                        category_words_list = None
                except:
                    category_words_list = None
                try:
                    keyword_words_list = front_input['keyword_words_list']
                    if keyword_words_list == '':
                        raise
                    try:
                        keyword_words_list = str(keyword_words_list).split(',')
                    except:
                        keyword_words_list = None
                except:
                    keyword_words_list = None
                try:
                    brand = front_input['brand']
                    if brand == '':
                        raise
                except:
                    brand = None
                try:
                    is_available = front_input['is_available']
                    if is_available == '':
                        raise
                    is_available = str(is_available).lower()
                    if is_available == 'true':
                        is_available = True
                    elif is_available == 'false':
                        is_available = False
                    else:
                        is_available = None
                except:
                    is_available = None
                try:
                    is_special = front_input['is_special']
                    if is_special == '':
                        raise
                    is_special = str(is_special).lower()
                    if is_special == 'true':
                        is_special = True
                    elif is_special == 'false':
                        is_special = False
                    else:
                        is_special = None
                except:
                    is_special = None
                try:
                    searched_word = front_input['searched_word']
                    if searched_word == '':
                        raise
                    searched_word = str(searched_word)
                except:
                    searched_word = None
                # print(f'date_range_from: {date_range_from}')
                # print(f'date_range_to: {date_range_to}')
                # print(f'price_range_from: {price_range_from}')
                # print(f'price_range_to: {price_range_to}')
                # print(f'score_range_from: {score_range_from}')
                # print(f'score_range_to: {score_range_to}')
                # print(f'brand: {brand}')
                # print(f'is_available: {is_available}')
                # print(f'is_special: {is_special}')
                # print(f'searched_word: {searched_word}')
                q = Q()
                if date_range_from and date_range_to:
                    q &= Q(**{f'created_at__range': [date_range_from, date_range_to]})
                if price_range_from and price_range_to:
                    q &= Q(**{f'total_price__gte': price_range_from})
                    q &= Q(**{f'total_price__lte': price_range_to})
                if score_range_from and score_range_to:
                    q &= Q(**{f'rating_score__gte': score_range_from})
                    q &= Q(**{f'rating_score__lte': score_range_to})
                if category_words_list:
                    q &= Q(**{f'categories__title_fa__in': category_words_list})
                if keyword_words_list:
                    q &= Q(**{f'keywords__title_fa__in': keyword_words_list})
                if brand:
                    q &= Q(**{f'brand': brand})
                if is_available is not None:
                    q &= Q(**{f'is_product_available': is_available})
                if is_special is not None:
                    q &= Q(**{f'is_product_special': is_special})
                if searched_word:
                    q &= (
                            Q(**{f'asin__icontains': searched_word}) |
                            Q(**{f'title_fa__icontains': searched_word}) |
                            Q(**{f'title_en__icontains': searched_word}) |
                            Q(**{f'description__icontains': searched_word}) |
                            Q(**{f'feature_bullets__icontains': searched_word}) |
                            Q(**{f'attributes__icontains': searched_word}) |
                            Q(**{f'specifications__icontains': searched_word})
                    )
                amazon_products = AmazonProduct.objects.filter(q)
                try:
                    page = request.GET['page']
                    paginator = PageNumberPagination()
                    paginator.page_size = 40
                    result_page = paginator.paginate_queryset(amazon_products, request)
                    serializer = AmazonProductSerializer(result_page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                except:
                    serializer = AmazonProductSerializer(amazon_products[:40], many=True)
                    return Response(serializer.data)

            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'فیلتر محصولات آمازون', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            return JsonResponse(create_json('post', 'فیلتر محصولات آمازون', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class CurrencyListView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        currencies = Currency.objects.filter()
        if currencies.count() == 0:
            return JsonResponse(create_json('post', 'لیست ارز', 'ناموفق', f'لیست ارز یافت نشد'))
        serializer = CurrencySerializer(currencies, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست ارز',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class BatoboxShippingListView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        batobox_shipping_list = BatoboxShipping.objects.filter()
        if batobox_shipping_list.count() == 0:
            return JsonResponse(
                create_json('post', 'لیست هزینه های حمل و نقل', 'ناموفق', f'لیست هزینه های حمل و نقل یافت نشد'))
        serializer = BatoboxShippingSerializer(batobox_shipping_list, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست هزینه های حمل و نقل',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class BatoboxCurrencyExchangeCommissionListView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        batobox_currency_exchange_commissions = BatoboxCurrencyExchangeCommission.objects.filter()
        if batobox_currency_exchange_commissions.count() == 0:
            return JsonResponse(
                create_json('post', 'لیست کمیسیون تبدیل ارز', 'ناموفق', f'لیست کمیسیون تبدیل ارز یافت نشد'))
        serializer = BatoboxCurrencyExchangeCommissionSerializer(batobox_currency_exchange_commissions, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست کمیسیون تبدیل ارز',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class CategoryListView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        categories = Category.objects.filter()
        if categories.count() == 0:
            return JsonResponse(create_json('post', 'لیست دسته', 'ناموفق', f'لیست دسته یافت نشد'))
        serializer = CategorySerializer(categories, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست دسته',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class OrderView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                pay_type = front_input['pay_type']  # pay_type = [wallet, direct]
                if not pay_type:
                    return JsonResponse(
                        create_json('post', 'ثبت سفارش', 'ناموفق', f'مقدار pay_type وارد نشده است'))
                if pay_type == 'wallet' or pay_type == 'direct':
                    pass
                else:
                    return JsonResponse(
                        create_json('post', 'ثبت سفارش', 'ناموفق', f'روش پرداخت با مقدار {pay_type} پشتیبانی نمی شود'))

                requested_products_id_list = front_input['requested_products_id_list']
                requested_products_id_list = str(requested_products_id_list).split(',')
                now = jdatetime.datetime.now()
                now_minus_15_minute = now - jdatetime.timedelta(minutes=15)
                request_item_list = []
                expired_products_id_list = []
                for requested_product_id in requested_products_id_list:
                    try:
                        requested_product = RequestedProduct.objects.get(id=requested_product_id)
                        if requested_product.created_at > now_minus_15_minute:
                            expired_products_id_list.append(requested_product_id)
                        else:
                            request_item_list.append(requested_product)
                    except:
                        return JsonResponse(
                            create_json('post', 'ثبت سفارش', 'ناموفق', f'محصول درخواستی با ایدی {requested_product_id} یافت نشد'))
                if len(expired_products_id_list) > 0:
                    return JsonResponse(
                        create_json('post', 'ثبت سفارش', 'ناموفق',
                                    f'محصولات درخواستی با ایدی [{",".join(expired_products_id_list)}] منقضی شده است'))
                if len(request_item_list) == 0:
                    return JsonResponse(
                        create_json('post', 'ثبت سفارش', 'ناموفق',
                                    f'محصولی انتخاب نشده است'))
                new_order = Order.objects.create(
                    order_status='در حال بررسی',
                    description='خرید محصول',
                    created_by=request.user,
                    updated_by=request.user,
                )
                amount = 0
                for request_item in request_item_list:
                    new_order.products.add(request_item)
                    new_order.save()
                    amount += request_item.final_price_in_toman
                new_uuid = str(uuid.uuid4())
                payment_unique_code = None
                if pay_type == 'wallet':
                    user_profile = request.user.user_profile
                    if user_profile.wallet_balance > amount:
                        payment_code = PaymentCode.objects.create(
                            user=request.user,
                            unique_code=new_uuid,
                            is_used=False,
                        )
                        payment_unique_code = new_uuid
                        authority = 'پرداخت محصولات از طریق اعتبار حساب'
                        ref_id = 'پرداخت محصولات از طریق اعتبار حساب'
                    else:
                        return JsonResponse(
                            create_json('post', 'ثبت سفارش', 'ناموفق', f'اعتبار حساب کافی نیست. مبلغ نهایی محصولات درخواستی برابر {amount} تومان میباشد و اعتبار حساب برابر {user_profile.wallet_balance} تومان می باشد. معادل {amount - user_profile.wallet_balance} تومان کسری اعتبار وجود دارد'))
                else:
                    try:
                        url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
                        header = {'Content-Type': 'application/json', 'accept': 'application/json'}
                        data = {
                            "merchant_id": ZARINPAL_API_KEY,
                            "amount": amount * 10,
                            "callback_url": f'{BASE_URL}store/api/pay-confirm/',
                            "description": f"فاکتور پرداختی توسط {request.user.username}",
                            "metadata": {"mobile": request.user.username}
                        }
                        pay_request = requests.post(url=url, data=json.dumps(data), headers=header)
                        if pay_request.status_code == 200:
                            authority = pay_request.json()['data']["authority"]
                            ref_id = 'پرداخت محصولات از طریق درگاه'
                            payment_code = PaymentCode.objects.create(
                                user=request.user,
                                unique_code=authority,
                                is_used=False,
                            )
                            payment_unique_code = authority
                        else:
                            return JsonResponse(
                                create_json('post', 'ثبت سفارش', 'ناموفق',
                                            f'خطای بازگشتی از درگاه پرداخت زرینپال با کد {pay_request.status_code}'))
                    except:
                        return JsonResponse(
                            create_json('post', 'ثبت سفارش', 'ناموفق', f'ارتباط با درگاه پرداخت زرین پال ممکن نیست'))

                new_transaction = Transaction.objects.create(
                    order=new_order,
                    amount=amount,
                    description=new_order.description,
                    email=request.user.email,
                    mobile=request.user.username,
                    authority=authority,
                    ref_id=ref_id,
                    status='در حال بررسی',
                )
                json_response_body = {
                    'method': 'post',
                    'request': 'ثبت سفارش',
                    'result': 'موفق',
                    'order_detail': {
                        'products': json.dumps(request_item_list),
                        'order_status': 'در حال بررسی',
                        'created_at': str(new_order.created_at),
                        'updated_at': str(new_order.updated_at),
                        'created_by': new_order.created_by.username,
                        'updated_by': new_order.updated_by.username,
                    },
                    'transaction_detail': {
                        'transaction_id': new_transaction.id,
                        'payment_unique_code': payment_unique_code
                    }
                }
                return JsonResponse(json_response_body)
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'ثبت سفارش', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'ثبت سفارش', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class RequestPayView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                pay_type = front_input['pay_type']  # pay_type = [wallet, direct]
                payment_unique_code = front_input['payment_unique_code']
                transaction_id = front_input['transaction_id']
                if pay_type == 'wallet' or pay_type == 'direct':
                    pass
                else:
                    return JsonResponse(
                        create_json('post', 'درخواست پرداخت', 'ناموفق', f'روش پرداخت با مقدار {pay_type} پشتیبانی نمی شود'))
                if payment_unique_code == '':
                    return JsonResponse(
                        create_json('post', 'درخواست پرداخت', 'ناموفق', f'مقدار payment_unique_code بدرستی ارسال نشده است'))
                else:
                    payment_code = PaymentCode.objects.filter(unique_code=payment_unique_code)
                    if payment_code.count() == 0:
                        return JsonResponse(
                            create_json('post', 'درخواست پرداخت', 'ناموفق',
                                        f'payment_unique_code ارسالی با مقدار {payment_unique_code} وجود ندارد'))
                    elif payment_code.count() == 1:
                        payment_code = payment_code[0]
                        if payment_code.is_used:
                            return JsonResponse(
                                create_json('post', 'درخواست پرداخت', 'ناموفق',
                                            f'payment_unique_code ارسالی با مقدار {payment_unique_code} استفاده شده است'))
                    else:
                        return JsonResponse(
                            create_json('post', 'درخواست پرداخت', 'ناموفق',
                                        f'payment_unique_code ارسالی با مقدار {payment_unique_code} امکان پرداخت ندارد. مجدد ثبت درخواست نمایید'))
                now = jdatetime.datetime.now()
                now_minus_15_minute = now - jdatetime.timedelta(minutes=15)
                try:
                    transaction = Transaction.objects.get(id=transaction_id)
                    if transaction.created_at < now_minus_15_minute:
                        return JsonResponse(
                            create_json('post', 'درخواست پرداخت', 'ناموفق', f'صورت حساب با ایدی {transaction_id}  منقضی شده است'))
                    if pay_type == 'wallet':
                        if transaction.ref_id == 'شارژ اعتبار حساب':
                            return JsonResponse(
                                create_json('post', 'درخواست پرداخت', 'ناموفق',
                                            f'امکان شارژ حساب از طریق شارژ حساب وجود ندارد'))
                        user_profile = request.user.user_profile
                        if user_profile.wallet_balance < transaction.amount:
                            return JsonResponse(
                                create_json('post', 'درخواست پرداخت', 'ناموفق',
                                            f'اعتبار حساب کافی نیست'))
                        payment_code.is_used = True
                        payment_code.save()
                        user_profile.wallet_balance -= transaction.amount
                        transaction.status = 'پرداخت شده'
                        transaction.save()
                        order = transaction.order
                        order.order_status = 'پرداخت شده و در انتظار بررسی'
                        order.save()
                        json_response_body = {
                            'method': 'post',
                            'request': 'درخواست پرداخت',
                            'result': 'موفق',
                            'transaction_detail': {
                                'need_pay': f'false',
                                'message': f'successfully payed from wallet',
                                'payment_gate_link': f'null',
                            }
                        }
                        return JsonResponse(json_response_body)
                    else:
                        json_response_body = {
                            'method': 'post',
                            'request': 'درخواست پرداخت',
                            'result': 'موفق',
                            'transaction_detail': {
                                'need_pay': f'true',
                                'message': f'the link of payment gate has been generated',
                                'payment_gate_link': f'https://www.zarinpal.com/pg/StartPay/{transaction.authority}',
                            }
                        }
                        return JsonResponse(json_response_body)
                except:
                    return JsonResponse(
                        create_json('post', 'درخواست پرداخت', 'ناموفق', f'صورت حساب با ایدی {transaction_id}  وجود ندارد'))
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'درخواست پرداخت', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'درخواست پرداخت', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class PayConfirmView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()
        self.context = {}

    def get(self, request, *args, **kwargs):
        authority = fetch_data_from_http_get(request, 'Authority', self.context)
        status = fetch_data_from_http_get(request, 'Status', self.context)
        if not status:
            return redirect(
                f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=not-valid-status')
        if status == 'NOK':
            return redirect(f'{BASE_FRONT_URL}profile?tab=wallet&status=nok')
        if not authority:
            return redirect(
                f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=not-valid-authority')
        else:
            payment_code = PaymentCode.objects.filter(unique_code=authority)
            if payment_code.count() == 0:
                return redirect(
                    f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=authority-not-found')
            elif payment_code.count() == 1:
                payment_code = payment_code[0]
                if payment_code.is_used:
                    return redirect(
                        f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=authority-can-accept-once')
            else:
                return redirect(
                    f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=authority-problem-request-pay-again')
        transaction = Transaction.objects.filter(authority=authority)
        if transaction.count() == 0:
            return redirect(f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=no-valid-authority-0')
        elif transaction.count() == 1:
            transaction = transaction[0]
            profile = transaction.order.created_by.user_profile
            try:
                url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
                header = {'Content-Type': 'application/json', 'accept': 'application/json'}
                data = {
                    "merchant_id": ZARINPAL_API_KEY,
                    "amount": transaction.amount * 10,
                    "authority": authority,
                }
                response = requests.post(url=url, json=data, headers=header)
                result = response.json()
                ref_id = None
                order = transaction.order
                try:
                    if int(result['data']['code']) == 100 or int(result['data']['code']) == 101:
                        if transaction.ref_id == 'شارژ اعتبار حساب':
                            profile.wallet_balance += transaction.amount
                            profile.save()
                            order.order_status = 'تکمیل شده'
                        else:
                            order.order_status = 'پرداخت شده و در انتظار بررسی'
                        ref_id = result['data']['ref_id']
                        transaction.ref_id = ref_id
                        transaction.status = 'پرداخت شده'
                    else:
                        transaction.status = 'پرداخت نشده'
                except Exception as e:
                    transaction.status = 'پرداخت نشده'
                transaction.save()
                order.save()
                payment_code.is_used = True
                payment_code.save()
                if status == 'پرداخت شده':
                    return redirect(f'{BASE_FRONT_URL}profile?tab=wallet&status=ok&ref-id={ref_id}')
                else:
                    return redirect(
                        f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=transaction-not-payed')
            except Exception as e:
                print(str(e))
                return redirect(
                    f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=zarinpal-verification-problem')
        else:
            return redirect(f'{BASE_FRONT_URL}profile?tab=wallet&status=nok&message=no-valid-authority-2')

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class OrderListView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        orders = Order.objects.filter(created_by=request.user)
        if orders.count() == 0:
            return JsonResponse(create_json('post', 'لیست سفارشات', 'ناموفق', f'لیست سفارشات یافت نشد'))
        serializer = OrderSerializer(orders, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست سفارشات',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class TransactionListView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(order__created_by=request.user)
        if transactions.count() == 0:
            return JsonResponse(create_json('post', 'لیست صورت حساب', 'ناموفق', f'لیست صورت حساب یافت نشد'))
        serializer = TransactionSerializer(transactions, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست صورت حساب',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})



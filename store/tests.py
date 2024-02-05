import requests
from batobox.settings import BASE_DIR, BASE_URL


def test_product_price_calculator_fetch_data():
    url = f'https://api.batobox.net/store/api/product-price-calculator/'

    product_link = 'https://www.amazon.ae/Andoer-Canceling-Gaming-Headset-Control/dp/B08319YFYW/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.f468f86c-3c20-47e1-91cd-bc7d1f3e4d76&pd_rd_r=8862014f-7925-407b-bd52-248b06800461&pd_rd_w=D0vws&pd_rd_wg=F96yw&pf_rd_p=f468f86c-3c20-47e1-91cd-bc7d1f3e4d76&pf_rd_r=HY6WHJ29C3S8EY2JP84D&qid=1707119236&s=electronics&sr=1-1&srs=88606009031'
    process_type = 'fetch_data_from_amazon'
    numbers = '1'
    description = 'دریافت داده در حالت دریافت  اطلاعات از رین فارست'

    headers = {
        'Authorization': 'BatoboxToken 6b50cacefd3d805de2f119dfbcb871c2d4d2767f0a94b466d4df4a27e53c1062'
    }
    data = {
        'product_link': product_link,
        'process_type': process_type,
        'numbers': numbers,
        'description': description,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_product_price_calculator_calculate_price_amazon_product():
    url = f'https://api.batobox.net/store/api/product-price-calculator/'

    product_link = 'https://www.amazon.ae/Andoer-Canceling-Gaming-Headset-Control/dp/B08319YFYW/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.f468f86c-3c20-47e1-91cd-bc7d1f3e4d76&pd_rd_r=8862014f-7925-407b-bd52-248b06800461&pd_rd_w=D0vws&pd_rd_wg=F96yw&pf_rd_p=f468f86c-3c20-47e1-91cd-bc7d1f3e4d76&pf_rd_r=HY6WHJ29C3S8EY2JP84D&qid=1707119236&s=electronics&sr=1-1&srs=88606009031'
    process_type = 'calculate_price'
    numbers = '2'
    description = 'دریافت داده در حالت دریافت  اطلاعات از رین فارست'

    headers = {
        'Authorization': 'BatoboxToken 6b50cacefd3d805de2f119dfbcb871c2d4d2767f0a94b466d4df4a27e53c1062'
    }

    data = {
        'product_link': product_link,
        'process_type': process_type,
        'numbers': numbers,
        'description': description,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_product_price_calculator_calculate_price_other_product():
    url = f'https://api.batobox.net/store/api/product-price-calculator/'

    product_link = 'https://zara.com/product_id=x25486df865'
    process_type = 'calculate_price'
    currency = 'AED'
    weight = '200'
    price = '100'
    numbers = '3'
    description = 'دریافت داده در حالت دریافت  اطلاعات از رین فارست'

    headers = {
        'Authorization': 'BatoboxToken 6b50cacefd3d805de2f119dfbcb871c2d4d2767f0a94b466d4df4a27e53c1062'
    }

    data = {
        'product_link': product_link,
        'process_type': process_type,
        'currency': currency,
        'weight': weight,
        'price': price,
        'numbers': numbers,
        'description': description,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_update_request_products():
    url = f'https://api.batobox.net/store/api/update-request-products/'

    request_product_id_list = '559,560'

    headers = {
        'Authorization': 'BatoboxToken 6b50cacefd3d805de2f119dfbcb871c2d4d2767f0a94b466d4df4a27e53c1062'
    }

    data = {
        'request_product_id_list': request_product_id_list,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def retriv_list_of_product(product_label, date_range_from=None, date_range_to=None, price_range_from=None,
                           price_range_to=None,
                           score_range_from=None, score_range_to=None, category_words_list=None,
                           keyword_words_list=None,
                           brand=None, is_available=None, is_special=None, searched_word=None):
    if not product_label:
        return print('product_label not found')
    url = f'{BASE_URL}store/api/product-list/'
    data = {
        'product_label': f'{product_label}',
        'date_range_from': f'{date_range_from}',
        'date_range_to': f'{date_range_to}',
        'price_range_from': f'{price_range_from}',
        'price_range_to': f'{price_range_to}',
        'score_range_from': f'{score_range_from}',
        'score_range_to': f'{score_range_to}',
        'category_words_list': f'{category_words_list}',
        'keyword_words_list': f'{keyword_words_list}',
        'brand': f'{brand}',
        'is_available': f'{is_available}',
        'is_special': f'{is_special}',
        'searched_word': f'{searched_word}',
    }
    try:
        response = requests.post(url, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def retriv_list_of_product_with_page(product_label, date_range_from=None, date_range_to=None, price_range_from=None,
                                     price_range_to=None,
                                     score_range_from=None, score_range_to=None, category_words_list=None,
                                     keyword_words_list=None,
                                     brand=None, is_available=None, is_special=None, searched_word=None,
                                     page_number=None):
    if not product_label:
        return print('product_label not found')
    url = f'{BASE_URL}store/api/product-list/?page={page_number}'
    data = {
        'product_label': f'{product_label}',
        'date_range_from': f'{date_range_from}',
        'date_range_to': f'{date_range_to}',
        'price_range_from': f'{price_range_from}',
        'price_range_to': f'{price_range_to}',
        'score_range_from': f'{score_range_from}',
        'score_range_to': f'{score_range_to}',
        'category_words_list': f'{category_words_list}',
        'keyword_words_list': f'{keyword_words_list}',
        'brand': f'{brand}',
        'is_available': f'{is_available}',
        'is_special': f'{is_special}',
        'searched_word': f'{searched_word}',
    }
    try:
        response = requests.post(url, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def retriv_single_product(product_id, amazon_product_asin):
    if not product_id:
        return print('product_id not found')
    if not amazon_product_asin:
        return print('amazon_product_asin not found')
    url = f'{BASE_URL}store/api/product/'
    data = {
        'product_id': f'{product_id}',
        'amazon_product_asin': f'{amazon_product_asin}',
    }
    try:
        response = requests.post(url, json=data)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_rain_forest_api(amazon_asin):
    params = {
        'api_key': 'C749DADEE54A40B695F423137F918325',
        'amazon_domain': 'amazon.ae',
        'asin': f'{amazon_asin}',
        'type': 'product'
    }
    try:
        product_api_data = requests.get('https://api.rainforestapi.com/request', params)
        with open(f'{amazon_asin}.json', 'w') as f:
            f.write(product_api_data.text)
        return print(f'the result can be found at: /var/www/batobox/{amazon_asin}.json')
    except Exception as e:
        print(str(e))


def test_get_currencies():
    url = f'{BASE_URL}store/api/currency/'
    try:
        response = requests.post(url)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_get_batobox_commission():
    url = f'{BASE_URL}store/api/batobox-commission/'
    try:
        response = requests.post(url)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_get_categories():
    url = f'{BASE_URL}store/api/categories/'
    try:
        response = requests.post(url)
        print(response.json())
    except Exception as e:
        print(str(e))


def test_get_keywords():
    url = f'{BASE_URL}store/api/keywords/'
    try:
        response = requests.post(url)
        print(response.json())
    except Exception as e:
        print(str(e))

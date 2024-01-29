import requests
from batobox.settings import BASE_DIR, BASE_URL


def test_product_price_calculator_fetch_data():
    url = f'https://api.batobox.net/store/api/product-price-calculator/'

    product_link = 'https://www.amazon.ae/Dell-Latitude-7490-Touchscreen-Business/dp/B0CL39CDW5'
    process_type = 'fetch_data_from_amazon'
    numbers = '1'
    description = 'دریافت داده در حالت دریافت  اطلاعات از رین فارست'

    headers = {
        'Authorization': 'BatoboxToken 7b34ed182060d88027f6481ccca976fa3ff53123acc852505f18a2f922ce8d51'
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

    product_link = 'https://www.amazon.ae/Dell-Latitude-7490-Touchscreen-Business/dp/B0CL39CDW5'
    process_type = 'calculate_price'
    numbers = '2'
    description = 'دریافت داده در حالت دریافت  اطلاعات از رین فارست'

    headers = {
        'Authorization': 'BatoboxToken 7b34ed182060d88027f6481ccca976fa3ff53123acc852505f18a2f922ce8d51'
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
        'Authorization': 'BatoboxToken 7b34ed182060d88027f6481ccca976fa3ff53123acc852505f18a2f922ce8d51'
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

    request_product_id_list = '310, 311'

    headers = {
        'Authorization': 'BatoboxToken 7b34ed182060d88027f6481ccca976fa3ff53123acc852505f18a2f922ce8d51'
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

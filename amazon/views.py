import os
import random
import threading
import time

from django.core.files.base import ContentFile
from django.utils.text import slugify
from googletrans import Translator
import requests
import json

from django.http import JsonResponse
from custom_logs.models import custom_log
from storage.models import Storage
from store.models import RainForestApiAccessHistory


def update_amazon_product_from_rainforest_api(amazon_product):
    if not amazon_product.asin:
        return JsonResponse({'message': 'no asin available or product'})
    # set up the request parameters
    params = {
        'api_key': 'C749DADEE54A40B695F423137F918325',
        'amazon_domain': 'amazon.ae',
        'asin': f'{amazon_product.asin}',
        'type': 'product'
    }
    try:
        product_api_data = requests.get('https://api.rainforestapi.com/request', params)
        product_api_data = product_api_data.json()
        # product_api_data = open('B0BQ5WG6CQ.json', 'r')
        # product_api_data = json.load(product_api_data)
        files_list = []
        try:
            request_info_success = product_api_data['request_info']['success']
            request_info_success = str(request_info_success).lower()
            if request_info_success == 'true':
                request_info_success = 'true'
            elif request_info_success == 'false':
                request_info_success = 'false'
            else:
                request_info_success = 'false'
            api_query_result = json.dumps(product_api_data['request_info'])
        except Exception as e:
            request_info_success = 'false'
            api_query_result = str(e)
        RainForestApiAccessHistory.objects.create(
            api_query_result=api_query_result,
            created_by=amazon_product.created_by
        )
        try:
            request_info_credits_remaining = product_api_data['request_info']['credits_remaining']
        except Exception as e:
            request_info_credits_remaining = None
        if request_info_success == 'false':
            api_response = {
                'request_info_success': 'false',
                'request_info_credits_remaining': request_info_credits_remaining,
            }
            return JsonResponse(api_response)
        try:
            request_parameters_amazon_domain = product_api_data['request_parameters']['amazon_domain']
        except Exception as e:
            request_parameters_amazon_domain = None
        try:
            request_parameters_asin = product_api_data['request_parameters']['asin']
        except Exception as e:
            request_parameters_asin = None
        try:
            request_parameters_type = product_api_data['request_parameters']['type']
        except Exception as e:
            request_parameters_type = None
        try:
            request_metadata_amazon_url = product_api_data['request_metadata']['amazon_url']
        except Exception as e:
            request_metadata_amazon_url = None
        title_fa = None
        try:
            product_title = product_api_data['product']['title']
            try:
                translator = Translator()
                title_fa = translator.translate(product_title, dest='fa').text
            except Exception as e:
                title_fa = None
        except Exception as e:
            product_title = None
        try:
            product_link = product_api_data['product']['link']
        except Exception as e:
            product_link = None
        try:
            product_brand = product_api_data['product']['brand']
        except Exception as e:
            product_brand = None
        try:
            product_brand_url = product_api_data['product']['sub_title']['link']
        except Exception as e:
            product_brand_url = None
        try:
            product_documents = product_api_data['product']['documents']
            for product_document in product_documents:
                product_document_name = product_document['name']
                product_document_link = product_document['link']
                files_list.append(['documents', product_document_name, product_document_link])
        except Exception as e:
            product_documents = None
        try:
            product_description = product_api_data['product']['description']
        except Exception as e:
            product_description = None
        try:
            product_rating = product_api_data['product']['rating']
        except Exception as e:
            product_rating = None
        try:
            product_ratings_total = product_api_data['product']['ratings_total']
        except Exception as e:
            product_ratings_total = None
        try:
            product_main_image_link = product_api_data['product']['main_image']['link']
            files_list.append(['main_image', f'{request_parameters_asin}-main-image', product_main_image_link])
        except Exception as e:
            product_main_image_link = None
        product_images_list = []
        try:
            product_images = product_api_data['product']['images']
            i = 0
            for image in product_images:
                product_images_list.append(image['link'])
                files_list.append(['images', f'{request_parameters_asin}-image-{i}', image['link']])
                i += 1
        except Exception as e:
            product_images = None
        try:
            product_keywords_flat = product_api_data['product']['keywords']
            product_keywords_flat = str(product_keywords_flat)
        except Exception as e:
            product_keywords_flat = None
        try:
            product_feature_bullets = product_api_data['product']['feature_bullets']
            product_feature_bullets = json.dumps(product_feature_bullets)
        except Exception as e:
            product_feature_bullets = None
        try:
            product_attributes = product_api_data['product']['attributes']
            product_attributes = json.dumps(product_attributes)
        except Exception as e:
            product_attributes = None
        try:
            product_specifications = product_api_data['product']['specifications']
            product_specifications = json.dumps(product_specifications)
        except Exception as e:
            product_specifications = None
        try:
            unit = None
            try:
                product_weight = product_api_data['product']['weight']
                product_weight = str(product_weight).lower()
                if product_weight.find('kilograms') != -1:
                    product_weight = product_weight.split('kilograms')[0].replace(' ', '')
                    unit = 'kilograms'
                elif product_weight.find('grams') != -1:
                    product_weight = product_weight.split('grams')[0].replace(' ', '')
                    unit = 'grams'
                else:
                    raise Exception
                accept_char = '0123456789.'
                accept_char_list = []
                for char in reversed(product_weight):
                    if accept_char.find(char) != -1:
                        accept_char_list.append(char)
                    else:
                        break
                product_weight = ''.join(reversed(accept_char_list))
            except:
                try:
                    product_weight = product_api_data['product']['dimensions']
                    product_weight = str(product_weight).lower()
                    if product_weight.find('kilograms') != -1:
                        product_weight = product_weight.split('kilograms')[0].replace(' ', '')
                        unit = 'kilograms'
                    elif product_weight.find('grams') != -1:
                        product_weight = product_weight.split('grams')[0].replace(' ', '')
                        unit = 'grams'
                    else:
                        raise Exception
                    accept_char = '0123456789.'
                    accept_char_list = []
                    for char in reversed(product_weight):
                        if accept_char.find(char) != -1:
                            accept_char_list.append(char)
                        else:
                            break
                    product_weight = ''.join(reversed(accept_char_list))
                except:
                    try:
                        product_weight = product_api_data['product']['specifications_flat']
                        product_weight = str(product_weight).lower()
                        if product_weight.find('kilograms') != -1:
                            product_weight = product_weight.split('kilograms')[0].replace(' ', '')
                            unit = 'kilograms'
                        elif product_weight.find('grams') != -1:
                            product_weight = product_weight.split('grams')[0].replace(' ', '')
                            unit = 'grams'
                        else:
                            raise Exception
                        accept_char = '0123456789.'
                        accept_char_list = []
                        for char in reversed(product_weight):
                            if accept_char.find(char) != -1:
                                accept_char_list.append(char)
                            else:
                                break
                        product_weight = ''.join(reversed(accept_char_list))
                    except:
                        raise Exception
            product_weight = str(product_weight).lower()
            if unit == 'kilograms':
                product_weight = int(round(float(product_weight) * 1000, 0))
            else:
                product_weight = int(round(float(product_weight), 0))
        except Exception as e:
            product_weight = None
        try:
            product_buybox_winner_price_currency = product_api_data['product']['buybox_winner']['price'][
                'currency']
        except Exception as e:
            product_buybox_winner_price_currency = None
        try:
            product_buybox_winner_price_value = product_api_data['product']['buybox_winner']['price']['value']
        except Exception as e:
            product_buybox_winner_price_value = None
        try:
            product_buybox_winner_shipping = product_api_data['product']['buybox_winner']['shipping']
            try:
                shipping_currency = product_buybox_winner_shipping['currency']
                shipping_value = product_buybox_winner_shipping['value']
                shipping_price = float(shipping_value)
            except:
                shipping_price = 0
        except Exception as e:
            shipping_price = 0
        try:
            total_price = product_buybox_winner_price_value + shipping_price
        except Exception as e:
            total_price = None
        api_response = {
            'request_info_success': 'true',
            'request_info_credits_remaining': request_info_credits_remaining,
            'amazon_product_root_domain': request_parameters_amazon_domain,
            'asin': request_parameters_asin,
            'product_type': request_parameters_type,
            'product_root_url': request_metadata_amazon_url,
            'title_en': product_title,
            'title_fa': title_fa,
            'product_main_url': product_link,
            'brand': product_brand,
            'brand_url': product_brand_url,
            'keywords_flat': product_keywords_flat,
            'documents': product_documents,
            'description': product_description,
            'rating_score': product_rating,
            'user_rating_count': product_ratings_total,
            'main_image': product_main_image_link,
            'images': product_images_list,
            'feature_bullets': product_feature_bullets,
            'attributes': product_attributes,
            'specifications': product_specifications,
            'weight': product_weight,
            'currency': product_buybox_winner_price_currency,
            'base_price': product_buybox_winner_price_value,
            'shipping_price': shipping_price,
            'total_price': total_price,
            'files_list': files_list,
        }
        try:
            amazon_product.amazon_product_root_domain = api_response['amazon_product_root_domain']
            amazon_product.product_root_url = api_response['product_root_url']
            amazon_product.product_main_url = api_response['product_main_url']
            amazon_product.product_type = api_response['product_type']
            amazon_product.title_fa = api_response['title_fa']
            amazon_product.title_en = api_response['title_en']
            amazon_product.keywords_flat = api_response['keywords_flat']
            amazon_product.slug_title = slugify(api_response['title_en'])
            amazon_product.description = api_response['description']
            amazon_product.brand = api_response['brand']
            amazon_product.product_brand_url = api_response['brand_url']
            amazon_product.user_rating_count = api_response['user_rating_count']
            amazon_product.rating_score = api_response['rating_score']
            amazon_product.feature_bullets = api_response['feature_bullets']
            amazon_product.attributes = api_response['attributes']
            amazon_product.weight = api_response['weight']
            amazon_product.specifications = api_response['specifications']
            amazon_product.currency = api_response['currency']
            amazon_product.base_price = api_response['base_price']
            amazon_product.shipping_price = api_response['shipping_price']
            amazon_product.total_price = api_response['total_price']
            amazon_product.save()
            DownloadFilesThread(amazon_product, api_response['files_list']).start()
        except Exception as e:
            custom_log(f'problem saving data into amazon product. err: {str(e)}')
            api_response['request_info_success'] = 'false'
            api_response['exception'] = f'problem saving data into amazon product. err: {str(e)}'
        return JsonResponse(api_response)
    except Exception as e:
        return JsonResponse({'message': f'the error occurs when trying to get data from rainforest. err: {str(e)}',
                             'request_info_success': 'false'})


class AmazonUpdateProductDetail(threading.Thread):
    def __init__(self, request, amazon_products):
        super().__init__()
        self.request = request
        self.amazon_products = amazon_products

    def run(self):
        for amazon_product in self.amazon_products:
            update_amazon_product_from_rainforest_api(amazon_product)
            time.sleep(5)
        return



class DownloadFilesThread(threading.Thread):
    def __init__(self, product, files_list):
        super().__init__()
        self.product = product
        self.files_list = files_list

    def run(self):
        for file in self.files_list:
            try:
                filename = os.path.basename(file[2])
                root, extension = os.path.splitext(filename)
                if file[0] == 'main_image':
                    if not self.product.main_image:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            self.product.main_image.save(f'{file[1]}{extension.lower()}', content)
                            self.product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
                elif file[0] == 'documents':
                    if self.product.documents.all().count() == 0:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            new_storage_file = Storage.objects.create(
                                alt=file[1],
                                created_by=self.product.updated_by
                            )
                            new_storage_file.file.save(f'{file[1]}{extension.lower()}', content)
                            self.product.documents.add(new_storage_file)
                            self.product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
                elif file[0] == 'images':
                    if self.product.images.all().count() == 0:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            new_storage_file = Storage.objects.create(
                                alt=file[1],
                                created_by=self.product.updated_by
                            )
                            new_storage_file.file.save(f'{file[1]}{extension.lower()}', content)
                            self.product.images.add(new_storage_file)
                            self.product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
            except Exception as e:
                print(f'the error has occurred when downloading the file {file[1]}. err: {str(e)}')


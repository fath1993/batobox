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

from amazon.models import Category
from custom_logs.models import custom_log
from storage.models import Storage
from store.models import RainForestApiAccessHistory


def update_amazon_product_from_rainforest_api(amazon_product):
    if not amazon_product.asin:
        return JsonResponse({'message': 'no asin available or product'})

    params = {
        'api_key': 'C749DADEE54A40B695F423137F918325',
        'amazon_domain': 'amazon.ae',
        'asin': f'{amazon_product.asin}',
        'type': 'product'
    }
    try:
        product_api_data = requests.get('https://api.rainforestapi.com/request', params)
        product_api_data = product_api_data.json()
        custom_log(product_api_data)
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
        if request_info_success == 'false':
            custom_log(api_query_result)
            return False
        try:
            request_parameters_amazon_domain = product_api_data['request_parameters']['amazon_domain']
            if str(request_parameters_amazon_domain) != '':
                amazon_product.amazon_product_root_domain = request_parameters_amazon_domain
        except Exception as e:
            pass
        try:
            request_parameters_asin = product_api_data['request_parameters']['asin']
        except Exception as e:
            pass
        try:
            request_parameters_type = product_api_data['request_parameters']['type']
            if str(request_parameters_type) != '':
                amazon_product.product_type = request_parameters_type
        except Exception as e:
            pass
        try:
            request_metadata_amazon_url = product_api_data['request_metadata']['amazon_url']
            if str(request_metadata_amazon_url) != '':
                amazon_product.product_root_url = request_metadata_amazon_url
        except Exception as e:
            pass
        try:
            product_title = product_api_data['product']['title']
            if str(product_title) != '':
                amazon_product.title_en = product_title
                amazon_product.slug_title = slugify(product_title)
                if not amazon_product.slug:
                    amazon_product.slug = slugify(product_title)
            try:
                translator = Translator()
                title_fa = translator.translate(product_title, dest='fa').text
                if str(title_fa) != '':
                    if not amazon_product.title_fa:
                        amazon_product.title_fa = title_fa
                    if not amazon_product.seo_title:
                        amazon_product.seo_title = title_fa
                    if not amazon_product.seo_description:
                        amazon_product.seo_description = title_fa
            except Exception as e:
                pass
        except Exception as e:
            pass
        try:
            product_link = product_api_data['product']['link']
            if str(product_link) != '':
                amazon_product.product_main_url = product_link
        except Exception as e:
            pass
        try:
            product_brand = product_api_data['product']['brand']
            if str(product_brand) != '':
                amazon_product.brand = product_brand
        except Exception as e:
            pass
        try:
            product_brand_url = product_api_data['product']['sub_title']['link']
            if str(product_brand_url) != '':
                amazon_product.product_brand_url = product_brand_url
        except Exception as e:
            pass
        try:
            product_documents = product_api_data['product']['documents']
            if str(product_documents) != '':
                try:
                    for product_document in product_documents:
                        try:
                            product_document_name = product_document['name']
                            product_document_link = product_document['link']
                            files_list.append(['documents', product_document_name, product_document_link])
                        except:
                            pass
                except:
                    pass
        except Exception as e:
            pass
        try:
            product_description = product_api_data['product']['description']
            if str(product_description) != '':
                amazon_product.description = product_description
        except Exception as e:
            pass
        try:
            product_rating = product_api_data['product']['rating']
            if str(product_rating) != '':
                amazon_product.rating_score = product_rating
        except Exception as e:
            pass
        try:
            product_ratings_total = product_api_data['product']['ratings_total']
            if str(product_ratings_total) != '':
                amazon_product.user_rating_count = product_ratings_total
        except Exception as e:
            pass
        try:
            product_main_image_link = product_api_data['product']['main_image']['link']
            files_list.append(['main_image', f'{amazon_product.asin}-main-image', product_main_image_link])
        except Exception as e:
            pass
        product_images_list = []
        try:
            product_images = product_api_data['product']['images']
            i = 0
            for image in product_images:
                product_images_list.append(image['link'])
                files_list.append(['images', f'{amazon_product.asin}-image-{i}', image['link']])
                i += 1
        except Exception as e:
            pass
        try:
            product_keywords_flat = product_api_data['product']['keywords']
            product_keywords_flat = str(product_keywords_flat)
            if product_keywords_flat != '':
                amazon_product.keywords_flat = product_keywords_flat
                if not amazon_product.seo_keywords:
                    amazon_product.seo_keywords = product_keywords_flat
        except Exception as e:
            pass
        try:
            product_feature_bullets = product_api_data['product']['feature_bullets']
            if str(product_feature_bullets) != '':
                amazon_product.feature_bullets = json.dumps(product_feature_bullets)
        except Exception as e:
            pass
        try:
            product_attributes = product_api_data['product']['attributes']
            if str(product_attributes) != '':
                amazon_product.attributes = json.dumps(product_attributes)
        except Exception as e:
            pass
        try:
            product_specifications = product_api_data['product']['specifications']
            if str(product_specifications) != '':
                amazon_product.specifications = json.dumps(product_specifications)
        except Exception as e:
            pass
        try:
            product_variants = product_api_data['product']['variants']
            if str(product_variants) != '':
                amazon_product.variants = json.dumps(product_variants)
        except Exception as e:
            pass
        try:
            product_variant_asins_flat = product_api_data['product']['variant_asins_flat']
            if str(product_variant_asins_flat) != '':
                amazon_product.variants_asins_flat = str(product_variant_asins_flat)
        except Exception as e:
            pass
        try:
            product_has_size_guide = product_api_data['product']['has_size_guide']
            if str(product_has_size_guide) != '':
                amazon_product.has_size_guide = str(product_has_size_guide)
        except Exception as e:
            pass
        try:
            product_size_guide_html = product_api_data['product']['size_guide_html']
            if str(product_size_guide_html) != '':
                amazon_product.size_guide_html = str(product_size_guide_html)
        except Exception as e:
            pass
        if not amazon_product.weight:
            amazon_product.weight = 0
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
                        unit = 'unknown'
                        product_weight = 0
            if unit == 'kilograms':
                product_weight = int(round(float(product_weight) * 1000, 0))
            elif unit == 'grams':
                product_weight = int(round(float(product_weight), 0))
            else:
                product_weight = 0
            if product_weight != 0:
                amazon_product.weight = product_weight
        except Exception as e:
            pass
        try:
            product_buybox_winner_price_currency = product_api_data['product']['buybox_winner']['price'][
                'currency']
            if str(product_buybox_winner_price_currency) != '':
                amazon_product.currency = product_buybox_winner_price_currency
        except Exception as e:
            pass
        discounted_price = 0
        amazon_product.discounted_price = 0
        try:
            product_buybox_winner_price_value = product_api_data['product']['buybox_winner']['price']['value']
            if str(product_buybox_winner_price_value) != '':
                discounted_price = product_buybox_winner_price_value

        except Exception as e:
            pass
        base_price = 0
        amazon_product.base_price = 0
        try:
            product_buybox_winner_rrp_value = product_api_data['product']['buybox_winner']['rrp']['value']
            if str(product_buybox_winner_rrp_value) != '':
                base_price = product_buybox_winner_rrp_value

        except Exception as e:
            pass

        shipping_price = 0
        amazon_product.shipping_price = 0
        try:
            product_buybox_winner_shipping = product_api_data['product']['buybox_winner']['shipping']
            try:
                shipping_currency = product_buybox_winner_shipping['currency']
                if str(shipping_currency) != '':
                    shipping_value = product_buybox_winner_shipping['value']
                    if str(shipping_value) != '':
                        try:
                            shipping_price = float(shipping_value)
                            amazon_product.shipping_price = shipping_price
                        except:
                            pass
            except:
                pass
        except Exception as e:
            pass

        if discounted_price != 0 and base_price != 0:
            amazon_product.discounted_price = float(discounted_price)
            amazon_product.base_price = float(base_price)
            amazon_product.total_price = float(discounted_price) + shipping_price
        elif discounted_price == 0 and base_price != 0:
            amazon_product.discounted_price = 0
            amazon_product.base_price = float(base_price)
            amazon_product.total_price = float(base_price) + shipping_price
        elif discounted_price != 0 and base_price == 0:
            amazon_product.base_price = float(discounted_price)
            amazon_product.discounted_price = 0
            amazon_product.total_price = float(discounted_price) + shipping_price
        else:
            amazon_product.base_price = 0
            amazon_product.discounted_price = 0
            amazon_product.total_price = 0
        amazon_product.save()
        # DownloadFilesThread(amazon_product, files_list).start()
        for file in files_list:
            try:
                filename = os.path.basename(file[2])
                root, extension = os.path.splitext(filename)
                if file[0] == 'main_image':
                    if not amazon_product.main_image:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            amazon_product.main_image.save(f'{file[1]}{extension.lower()}', content)
                            amazon_product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
                elif file[0] == 'documents':
                    if not amazon_product.downloaded_documents:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            new_storage_file = Storage.objects.create(
                                alt=file[1],
                                created_by=amazon_product.updated_by
                            )
                            new_storage_file.file.save(f'{file[1]}{extension.lower()}', content)
                            amazon_product.documents.add(new_storage_file)
                            amazon_product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
                elif file[0] == 'images':
                    if not amazon_product.downloaded_images:
                        response = requests.get(file[2], stream=True)
                        if response.status_code == 200:
                            content = ContentFile(response.content)
                            new_storage_file = Storage.objects.create(
                                alt=file[1],
                                created_by=amazon_product.updated_by
                            )
                            new_storage_file.file.save(f'{file[1]}{extension.lower()}', content)
                            amazon_product.images.add(new_storage_file)
                            amazon_product.save()
                            print(f"successfully received file {file[1]}")
                        else:
                            print(f"Failed to download image. Status code: {response.status_code}")
                        time.sleep(1)
            except Exception as e:
                print(f'the error has occurred when downloading the file {file[1]}. err: {str(e)}')
        amazon_product.downloaded_documents = True
        amazon_product.downloaded_images = True
        amazon_product.save()
        if amazon_product.categories.all().count() == 0:
            default_category = Category.objects.get_or_create(
                title_fa='بدون دسته',
                title_en='uncategorized',
            )
            amazon_product.categories.add(default_category[0])
            amazon_product.save()
        return amazon_product
    except Exception as e:
        custom_log(f'the error occurs when trying to get data from rainforest. err: {str(e)}')
        return False


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




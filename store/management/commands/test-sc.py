from django.core.management import base

from store.tests import test_create_new_product, test_rain_forest_api, retriv_list_of_product, retriv_single_product, \
    retriv_list_of_product_with_page, test_get_currencies, test_get_batobox_commission, test_get_categories, \
    test_get_keywords


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        while True:
            print('what do you need?')
            print('1. check creating new product')
            print('2. retriv list of products')
            print('3. retriv single product by asin')
            print('4. test result of rainforest api by asin')
            print('5. retriv list of currencies')
            print('6. retriv list of batobox commissions')
            print('7. retriv list of categories')
            print('8. retriv list of keywords')
            try:
                choice = int(input())
                if choice == 1:
                    print('please input asin:')
                    asin = str(input())
                    print('please input currency:')
                    currency = str(input())
                    print('please input weight:')
                    weight = str(input())
                    print('please input price:')
                    price = str(input())
                    print('please input description:')
                    description = str(input())
                    test_create_new_product(amazon_asin=asin, currency=currency, weight=weight, price=price,
                                            description=description)
                elif choice == 2:
                    print('necessary data: product_label->amazon')
                    print('optional data: product_label, date_range_from, date_range_to,'
                          ' price_range_from, price_range_to, score_range_from, score_range_to,'
                          ' category_words_list, keyword_words_list, brand, is_available, is_special, searched_word, page_number')
                    print('please input product_label:')
                    product_label = str(input())
                    print('please input date_range_from: like->1402/10/05/14:00')
                    date_range_from = str(input())
                    print('please input date_range_to: like->1402/10/05/14:00')
                    date_range_to = str(input())
                    print('please input price_range_from:')
                    price_range_from = str(input())
                    print('please input price_range_to:')
                    price_range_to = str(input())
                    print('please input score_range_from:')
                    score_range_from = str(input())
                    print('please input score_range_to:')
                    score_range_to = str(input())
                    print('please input category_words_list:')
                    category_words_list = str(input())
                    print('please input keyword_words_list:')
                    keyword_words_list = str(input())
                    print('please input brand:')
                    brand = str(input())
                    print('please input is_available: like->true')
                    is_available = str(input())
                    print('please input is_special: like->true')
                    is_special = str(input())
                    print('please input searched_word: could be anything')
                    searched_word = str(input())
                    print('please input page number')
                    page_number = str(input())
                    retriv_list_of_product_with_page(product_label=product_label, date_range_from=date_range_from,
                                                     date_range_to=date_range_to, price_range_from=price_range_from,
                                                     price_range_to=price_range_to,
                                                     score_range_from=score_range_from, score_range_to=score_range_to,
                                                     category_words_list=category_words_list,
                                                     keyword_words_list=keyword_words_list,
                                                     brand=brand, is_available=is_available, is_special=is_special,
                                                     searched_word=searched_word, page_number=page_number)
                elif choice == 3:
                    print('please input product_id:')
                    product_id = str(input())
                    print('please input amazon_product_asin:')
                    amazon_product_asin = str(input())
                    retriv_single_product(product_id, amazon_product_asin)
                elif choice == 4:
                    print('please input amazon_asin:')
                    amazon_asin = str(input())
                    test_rain_forest_api(amazon_asin)
                elif choice == 5:
                    test_get_currencies()
                elif choice == 6:
                    test_get_batobox_commission()
                elif choice == 7:
                    test_get_categories()
                elif choice == 8:
                    test_get_keywords()
                else:
                    print('ورودی صحیح نیست مجدد امتحان کنید')
            except Exception as e:
                print(f'err: {str(e)}')
                print('ورودی صحیح نیست مجدد امتحان کنید')

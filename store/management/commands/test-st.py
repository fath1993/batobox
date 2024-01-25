from django.core.management import base

from store.tests import test_rain_forest_api, retriv_list_of_product, retriv_single_product, \
    retriv_list_of_product_with_page, test_get_currencies, test_get_batobox_commission, test_get_categories, \
    test_get_keywords, test_product_price_calculator_fetch_data, \
    test_product_price_calculator_calculate_price_other_product, \
    test_product_price_calculator_calculate_price_amazon_product, test_update_request_products


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        while True:
            print('what do you need?')
            print('1. check test_product_price_calculator_fetch_data')
            print('2. check test_product_price_calculator_calculate_price_amazon_product')
            print('3. check test_product_price_calculator_calculate_price_other_product')
            print('4. check test_update_request_products')
            print('5. retriv single product by asin')
            print('6. test result of rainforest api by asin')
            print('7. retriv list of currencies')
            print('8. retriv list of batobox commissions')
            print('9. retriv list of categories')
            print('10. retriv list of keywords')
            try:
                choice = int(input())
                if choice == 1:
                    test_product_price_calculator_fetch_data()
                elif choice == 2:
                    test_product_price_calculator_calculate_price_amazon_product()
                elif choice == 3:
                    test_product_price_calculator_calculate_price_other_product()
                elif choice == 4:
                    test_update_request_products()
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

from django.core.management import base

from amazon.tests import text_get_sample_product_from_rain_forest_api


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        text_get_sample_product_from_rain_forest_api()

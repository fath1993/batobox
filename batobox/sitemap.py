from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# from products.models import Product


class StaticViewSitemap(Sitemap):
    name = 'static'
    protocol = 'https'

    def items(self):
        return ['home-page', 'product-list-page', 'contact-us-page', 'turkey-page', 'uae-page', 'terms-and-conditions',
                'frequently-asked-questions', 'about-us-page']

    def location(self, item):
        return reverse(item)


class ProductListSitemap(Sitemap):
    name = 'product'
    protocol = 'https'
    property = 1.0
    changefreq = 'daily'

    def items(self):
        product_list = []
        # q = Product.objects.filter(special_product=True)
        q = None
        for item in q:
            product_list.append((item.id, item.slug))
        return product_list

    def location(self, item):
        return reverse('product-single-page', kwargs={'pk': item[0], 'slug': item[1]})

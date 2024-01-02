from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views
from django.views.generic import RedirectView

from website.views import landing_view

# from batobox.sitemap import StaticViewSitemap, ProductListSitemap
#
# sitemaps = {
#     StaticViewSitemap.name: StaticViewSitemap,
#     ProductListSitemap.name: ProductListSitemap,
# }

app_name = 'batobox'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),
    path('captcha/', include('captcha.urls')),
    path('account/', include('accounts.urls')),
    path('docs/', include('docs.urls')),
    path('store/', include('store.urls')),
    path('website/', include('website.urls')),
    path('ticket/', include('ticket.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# urlpatterns += [
#     path(
#         'sitemap.xml',
#         cache_page(86400)(sitemaps_views.index),
#         {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'},
#     ),
#     path(
#         'sitemap-<section>.xml',
#         cache_page(86400)(sitemaps_views.sitemap),
#         {'sitemaps': sitemaps},
#         name='sitemaps',
#     ),
# ]
#
#

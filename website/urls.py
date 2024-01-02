from django.urls import path, include

from website.views import BannerTopHeaderView, BannerTopFooterView, BannerMiddleFooterView, HomePageSliderView, \
    WhyUsReasonView, FrequentlyAskedQuestionView, TermAndConditionView, PageSeoView, WebsiteView, DynamicDataView, \
    BrandView

app_name = 'website'

urlpatterns = [
    path('api/banner-top-header/', BannerTopHeaderView.as_view(), name='banner-top-header'),
    path('api/banner-top-footer/', BannerTopFooterView.as_view(), name='banner-top-footer'),
    path('api/banner-middle-footer/', BannerMiddleFooterView.as_view(), name='banner-middle-footer'),
    path('api/home-page-slider/', HomePageSliderView.as_view(), name='home-page-slider'),
    path('api/why-us-reason/', WhyUsReasonView.as_view(), name='why-us-reason'),
    path('api/frequently-asked-question/', FrequentlyAskedQuestionView.as_view(), name='frequently-asked-question'),
    path('api/term-and-condition/', TermAndConditionView.as_view(), name='term-and-condition'),
    path('api/page-seo/', PageSeoView.as_view(), name='page-seo'),
    path('api/website/', WebsiteView.as_view(), name='website'),
    path('api/brands/', BrandView.as_view(), name='brands'),
    path('api/dynamic-data/', DynamicDataView.as_view(), name='dynamic-data'),
]




















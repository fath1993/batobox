from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from utilities.utilities import create_json
from website.models import BannerTopHeader, WhyUsReason, HomePageSlider, BannerMiddleFooter, BannerTopFooter, \
    FrequentlyAskedQuestion, TermAndCondition, PageSeo, Website, DynamicData, Brand
from website.serializer import BannerTopHeaderSerializer, BannerTopFooterSerializer, BannerMiddleFooterSerializer, \
    HomePageSliderSerializer, WhyUsReasonSerializer, FrequentlyAskedQuestionSerializer, TermAndConditionSerializer, \
    PageSeoSerializer, WebsiteSerializer, DynamicDataSerializer, BrandSerializer


def landing_view(request):
    return render(request, '404.html')


class BannerTopHeaderView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'بنر هدر'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        banners_top_header = BannerTopHeader.objects.filter()
        if banners_top_header.count() == 0:
            return JsonResponse(create_json('post', 'بنر هدر', 'ناموفق', f'بنر هدر یافت نشد'))
        serializer = BannerTopHeaderSerializer(banners_top_header, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'بنر هدر',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class BannerTopFooterView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'بنر بالای فوتر'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        banners_top_footer = BannerTopFooter.objects.filter()
        if banners_top_footer.count() == 0:
            return JsonResponse(create_json('post', 'بنر بالای فوتر', 'ناموفق', f'بنر بالای فوتر یافت نشد'))
        serializer = BannerTopFooterSerializer(banners_top_footer, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'بنر بالای فوتر',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class BannerMiddleFooterView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'بنر میانه فوتر'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        banners_middle_footer = BannerMiddleFooter.objects.filter()
        if banners_middle_footer.count() == 0:
            return JsonResponse(create_json('post', 'بنر میانه فوتر', 'ناموفق', f'بنر میانه فوتر یافت نشد'))
        serializer = BannerMiddleFooterSerializer(banners_middle_footer, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'بنر هدر',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class HomePageSliderView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'اسلایدر صفحه اصلی'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        home_page_sliders = HomePageSlider.objects.filter()
        if home_page_sliders.count() == 0:
            return JsonResponse(create_json('post', 'اسلایدر صفحه اصلی', 'ناموفق', f'اسلایدر صفحه اصلی یافت نشد'))
        serializer = HomePageSliderSerializer(home_page_sliders, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'اسلایدر صفحه اصلی',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class WhyUsReasonView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'دلایل انتخاب ما'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        why_us_reasons = WhyUsReason.objects.filter()
        if why_us_reasons.count() == 0:
            return JsonResponse(create_json('post', 'بنر هدر', 'ناموفق', f'دلایل انتخاب ما یافت نشد'))
        serializer = WhyUsReasonSerializer(why_us_reasons, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'دلایل انتخاب ما',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class FrequentlyAskedQuestionView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'سوالات متداول'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        frequently_asked_questions = FrequentlyAskedQuestion.objects.filter()
        if frequently_asked_questions.count() == 0:
            return JsonResponse(create_json('post', 'سوالات متداول', 'ناموفق', f'سوالات متداول یافت نشد'))
        serializer = FrequentlyAskedQuestionSerializer(frequently_asked_questions, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'سوالات متداول',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class TermAndConditionView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'شرایط و قوانین'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        terms_and_conditions = TermAndCondition.objects.filter()
        if terms_and_conditions.count() == 0:
            return JsonResponse(create_json('post', 'شرایط و قوانین', 'ناموفق', f'شرایط و قوانین یافت نشد'))
        serializer = TermAndConditionSerializer(terms_and_conditions, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'شرایط و قوانین',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class PageSeoView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'جزئیات سئوی صفحات'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        page_seo_details = PageSeo.objects.filter()
        if page_seo_details.count() == 0:
            return JsonResponse(create_json('post', 'جزئیات سئوی صفحات', 'ناموفق', f'جزئیات سئوی صفحات یافت نشد'))
        serializer = PageSeoSerializer(page_seo_details, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'جزئیات سئوی صفحات',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class WebsiteView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'سایت ها'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        websites = Website.objects.filter()
        if websites.count() == 0:
            return JsonResponse(create_json('post', 'سایت ها', 'ناموفق', f'سایت ها یافت نشد'))
        serializer = WebsiteSerializer(websites, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'سایت ها',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class BrandView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'لیست برند'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        brands = Brand.objects.filter()
        if brands.count() == 0:
            return JsonResponse(create_json('post', 'لیست برند', 'ناموفق', f'لیست برند یافت نشد'))
        serializer = BrandSerializer(brands, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست برند',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class DynamicDataView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'داینامیک دیتا'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        dynamic_data = DynamicData.objects.filter()
        if dynamic_data.count() == 0:
            return JsonResponse(create_json('post', 'داینامیک دیتا', 'ناموفق', f'داینامیک دیتا یافت نشد'))
        serializer = DynamicDataSerializer(dynamic_data, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'داینامیک دیتا',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


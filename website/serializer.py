from rest_framework import serializers

from website.models import BannerTopHeader, BannerTopFooter, BannerMiddleFooter, HomePageSlider, WhyUsReason, \
    FrequentlyAskedQuestion, TermAndCondition, PageSeo, Website, DynamicData, Brand


class BannerTopHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerTopHeader
        fields = "__all__"


class BannerTopFooterSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerTopFooter
        fields = "__all__"


class BannerMiddleFooterSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerMiddleFooter
        fields = "__all__"


class HomePageSliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePageSlider
        fields = "__all__"


class WhyUsReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyUsReason
        fields = "__all__"


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"


class TermAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = "__all__"


class PageSeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSeo
        fields = "__all__"


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class DynamicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicData
        fields = "__all__"


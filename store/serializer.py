from rest_framework import serializers
from store.models import Currency, BatoboxShipping, BatoboxCurrencyExchangeCommission


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"


class BatoboxShippingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BatoboxShipping
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['currency'] = instance.currency.badge
        return ret


class BatoboxCurrencyExchangeCommissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BatoboxCurrencyExchangeCommission
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['currency'] = instance.currency.badge
        return ret
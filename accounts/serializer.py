from rest_framework import serializers

from accounts.models import Order, Transaction


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.crated_by.username
        ret['updated_by'] = instance.updated_by.username
        return ret

    class Meta:
        model = Order
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

import json

from rest_framework import serializers
from amazon.models import AmazonProduct, Keyword, Category
from storage.serializer import StorageSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = "__all__"


class AmazonProductSerializer(serializers.ModelSerializer):
    images = StorageSerializer(many=True)
    documents = StorageSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = AmazonProduct
        fields = "__all__"


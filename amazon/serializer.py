import json

from rest_framework import serializers
from amazon.models import AmazonProduct, Keyword, Category
from storage.serializer import StorageSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        child_category = Category.objects.filter(parent=instance)
        children_data = []
        for child in child_category:
            try:
                cat_image = child.cat_image.url
            except:
                cat_image = None
            children_data.append({
                'id': child.id,
                'title_fa': child.title_fa,
                'title_en': child.title_en,
                'title_slug': child.title_slug,
                'cat_image': cat_image,
            })
        ret['children'] = json.dumps(children_data)
        return ret


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = "__all__"


class AmazonProductSerializer(serializers.ModelSerializer):
    images = StorageSerializer(many=True)

    class Meta:
        model = AmazonProduct
        fields = "__all__"


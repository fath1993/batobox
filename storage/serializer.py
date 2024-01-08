from rest_framework import serializers

from batobox.settings import BASE_URL
from storage.models import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['file'] = f"{BASE_URL}{instance.file.url}"
        return ret
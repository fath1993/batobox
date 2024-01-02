from rest_framework import serializers

from storage.serializer import StorageSerializer
from ticket.models import Ticket, Message


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        return ret


class MessageSerializer(serializers.ModelSerializer):
    attachments = StorageSerializer(many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.created_by.username
        return ret

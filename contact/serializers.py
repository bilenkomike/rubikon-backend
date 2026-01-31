from rest_framework.serializers import ModelSerializer
from .models import Contact


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "email",
            "message",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer


class ContactCreateAPIView(CreateAPIView):
    """
    Public API to send contact / feedback message
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

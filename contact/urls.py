from django.urls import path
from .views import ContactCreateAPIView

urlpatterns = [
    path("", ContactCreateAPIView.as_view(), name="contact-create"),
]

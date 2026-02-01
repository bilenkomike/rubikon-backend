from django.urls import path
from .views import (
    CartListAPIView,
    CartAddAPIView,
    CartUpdateAPIView,
    CartRemoveAPIView,
    CheckoutAPIView,
    OrderListAPIView,
    OrderRetrieveAPIView,
)


urlpatterns = [
    path("cart/", CartListAPIView.as_view()),
    path("cart/add/", CartAddAPIView.as_view()),
    path("cart/<int:pk>/", CartUpdateAPIView.as_view()),
    path("cart/<int:pk>/remove/", CartRemoveAPIView.as_view()),
    path("checkout/", CheckoutAPIView.as_view()),
    path("", OrderListAPIView.as_view()),
    path("<int:pk>/", OrderRetrieveAPIView.as_view()),
]

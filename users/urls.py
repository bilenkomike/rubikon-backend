from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginAPIView, RegisterAPIView, MeAPIView, WishlistAddAPIView, WishlistRemoveAPIView, ChangePasswordAPIView, WishlistListAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", LoginAPIView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path(
        "wishlist/",
        WishlistListAPIView.as_view(),
        name="wishlist-list",
    ),
    path(
        "wishlist/add/",
        WishlistAddAPIView.as_view(),
        name="wishlist-add",
    ),
    path(
        "wishlist/remove/<int:product_id>/",
        WishlistRemoveAPIView.as_view(),
        name="wishlist-remove",
    ),
    path(
        "me/",
        MeAPIView.as_view(),
        name="users-me",
    ),
]
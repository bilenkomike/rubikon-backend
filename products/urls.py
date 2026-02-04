from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductReviewListAPIView,
    ProductReviewCreateAPIView,
    CategoryListAPIView,
    SubCategoryRetrieveAPIView,
    SubCategoryListAPIView,
    FilterListAPIView,
    CategoryRetrieveAPIView,
    BannersListAPIView,
    ProductSearchAPIView,
)


urlpatterns = [
    path("banners/", BannersListAPIView.as_view()),
    path("categories/", CategoryListAPIView.as_view()),
    path("search/", ProductSearchAPIView.as_view()),
    path(
      "categories/<slug:slug>/",
        CategoryRetrieveAPIView.as_view(),
    ),
    path(
        "categories/subcategories/<slug:slug>/",
        SubCategoryRetrieveAPIView.as_view(),
    ),
    path(
        "categories/<slug:slug>/subcategories/",
        SubCategoryListAPIView.as_view(),
        name="subcategory-list",
    ),
    path("filters/", FilterListAPIView.as_view(), name="filter-list"),
    path("", ProductListAPIView.as_view()),
    path("<slug:slug>/", ProductDetailAPIView.as_view()),
    path("<slug:slug>/reviews/", ProductReviewListAPIView.as_view()),
    path("<slug:slug>/reviews/create/", ProductReviewCreateAPIView.as_view()),

]

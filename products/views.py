from django.db.models import Min, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.db.models import Value
from .models import (
    Product,
    Category,
    SubCategory,
    FilterType,
    ProductStatistic,
)
from .serializers import (
    ProductSmallSerializer,
    ProductBigSerializer,
    ProductReviewSerializer,
    ProductReview,
    CategorySerializer,
    SubCategorySerializer,
    FilterTypeWithValuesSerializer,
)
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 48
    page_size_query_param = None
    max_page_size = 48


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSmallSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related("category", "statistics")
            .prefetch_related("productimage_set", "filters")
        )

        params = self.request.query_params

        # 🔥 HOME PAGE (TRENDING)
        if params.get("home") in {"1", "true", "True"}:
            return qs.order_by("-statistics__sold")

        subcategory = params.get("subcategory")
        if subcategory:
            qs = qs.filter(category__slug=subcategory)

        filters = params.get("filters")
        if filters:
            filter_ids = [int(f) for f in filters.split(",") if f.isdigit()]
            if filter_ids:
                qs = qs.filter(filters__id__in=filter_ids).distinct()

        price_min = params.get("price_min")
        if price_min:
            qs = qs.filter(price__gte=price_min)

        price_max = params.get("price_max")
        if price_max:
            qs = qs.filter(price__lte=price_max)

        return qs.order_by("-created_at")


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductBigSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Product.objects
            .select_related(
                "category",
                "statistics",
            )
            .prefetch_related(
                "filters",
                "productimage_set",
                "productproperty_set",
                "productdescriptionitem_set",
            )
        )

    def get_object(self):
        product = super().get_object()

        ProductStatistic.objects.filter(
            product=product
        ).update(
            views=F("views") + 1
        )

        return product


class ProductReviewListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return (
            ProductReview.objects
            .filter(
                product__slug=self.kwargs["slug"],
                rating__gte=4,
            )
            .order_by("-created_at")[:10]
        )


class ProductReviewCreateAPIView(CreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs["slug"])
        serializer.save(product=product)


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Category.objects.annotate(
                _views=Coalesce(
                    Sum("subcategory__product__statistics__views"),
                    Value(0),
                )
            ).order_by("-_views")
        if self.request.query_params.get("home"):
            queryset = queryset[:10]
        return queryset


class SubCategoryListAPIView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return (
            SubCategory.objects
            .filter(category__slug=self.kwargs["slug"])
            .annotate(
                _views=Coalesce(
                    Sum("product__statistics__views"),
                    Value(0),
                )
            )
            .order_by("-_views")
        )


class FilterListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        subcategory_slug = request.query_params.get("subcategory")
        if not subcategory_slug:
            raise ValidationError({
                "subcategory": "This query param is required (subcategory=<slug>)"
            })

        # 🔹 get subcategory once
        subcategory = SubCategory.objects.filter(
            slug=subcategory_slug
        ).first()

        if not subcategory:
            raise ValidationError({
                "subcategory": "Invalid subcategory slug"
            })

        # 🔹 filters linked to this subcategory
        filters = (
            FilterType.objects
            .filter(category=subcategory)
            .prefetch_related("filtervalue_set")
            .order_by("id")
        )

        # 🔹 price range from products in this subcategory
        price = (
            Product.objects
            .filter(category=subcategory)
            .aggregate(
                min_price=Min("price"),
                max_price=Max("price"),
            )
        )

        return Response({
            "min_price": price["min_price"],
            "max_price": price["max_price"],
            "filters": FilterTypeWithValuesSerializer(filters, many=True).data,
        })

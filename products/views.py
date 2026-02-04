from django.db.models import Min, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Sum, F
from django.db.models import Q, Count, Case, When, IntegerField, Value

from django.db.models.functions import Coalesce
from django.db.models import Value
from .models import (
    Product,
    Category,
    SubCategory,
    FilterType,
    ProductStatistic,
    PromoBanner,
)
from .serializers import (
    ProductSmallSerializer,
    ProductBigSerializer,
    ProductReviewSerializer,
    ProductReview,
    CategorySerializer,
    SubCategorySerializer,
    FilterTypeWithValuesSerializer,
    PromoBannerSerializer,
)
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 48
    page_size_query_param = None
    max_page_size = 48


# class ProductListAPIView(ListAPIView):
#     serializer_class = ProductSmallSerializer
#     permission_classes = [AllowAny]
#     pagination_class = ProductPagination
#
#     def get_queryset(self):
#         qs = (
#             Product.objects
#             .select_related("category", "statistics")
#             .prefetch_related("productimage_set", "filters")
#         )
#
#         params = self.request.query_params
#
#         # 🔥 HOME PAGE (TRENDING)
#         if params.get("home") in {"1", "true", "True"}:
#             return qs.order_by("-statistics__sold")
#
#         subcategory = params.get("subcategory")
#         if subcategory:
#             qs = qs.filter(category__slug=subcategory)
#
#         # filters = params.get("filters")
#         # if filters:
#         #     filter_ids = [int(f) for f in filters.split(",") if f.isdigit()]
#         #     if filter_ids:
#         #         qs = qs.filter(filters__id__in=filter_ids).distinct()
#         filters = params.get("filters")
#         if filters:
#             filter_ids = [int(f) for f in filters.split(",") if f.isdigit()]
#
#             if filter_ids:
#                 qs = (
#                     qs.filter(filters__id__in=filter_ids)
#                     .annotate(
#                         matched_filters=Count(
#                             "filters",
#                             filter=Q(filters__id__in=filter_ids),
#                             distinct=True,
#                         )
#                     )
#                     .filter(matched_filters=len(filter_ids))
#                 )
#
#         price_min = params.get("price_min")
#         if price_min:
#             qs = qs.filter(price__gte=price_min)
#
#         price_max = params.get("price_max")
#         if price_max:
#             qs = qs.filter(price__lte=price_max)
#
#         return qs.order_by("-created_at")


class ProductSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("search")

        if not query:
            raise ValidationError({"search": "Search query is required"})

        q = query.strip()

        # -----------------------------
        # 1. SubCategory relevance
        # -----------------------------
        subcategories = (
            SubCategory.objects
            .annotate(
                relevance=Case(
                    When(name__iexact=q, then=Value(10)),
                    When(name_ru__iexact=q, then=Value(10)),
                    When(name__icontains=q, then=Value(5)),
                    When(name_ru__icontains=q, then=Value(5)),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                product_hits=Count(
                    "product",
                    filter=Q(product__name__icontains=q) |
                           Q(product__name_ru__icontains=q),
                    distinct=True,
                ),
            )
            .filter(
                Q(name__icontains=q) |
                Q(name_ru__icontains=q) |
                Q(product__name__icontains=q) |
                Q(product__name_ru__icontains=q)
            )
            .order_by("-relevance", "-product_hits")
            .distinct()
        )

        best_subcategory = subcategories.first()


        return Response(SubCategorySerializer(best_subcategory).data if best_subcategory else None)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSmallSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    def get_queryset(self):
        params = self.request.query_params

        qs = (
            Product.objects
            .select_related("category", "statistics")
            .prefetch_related("productimage_set", "filters")
        )

        # 🔥 HOME PAGE (TRENDING)
        if params.get("home") in {"1", "true", "True"}:
            return qs.order_by("-statistics__sold")

        subcategory_slug = params.get("subcategory")
        search = params.get("search")

        if not subcategory_slug and not search:
            raise ValidationError({
                "detail": "Either 'subcategory' or 'search' query param is required"
            })

        # 🔍 SEARCH FLOW → resolve closest subcategory
        if search:
            subcategory = (
                SubCategory.objects
                .annotate(
                    relevance=Case(
                        When(name__iexact=search, then=3),
                        When(name_ru__iexact=search, then=3),
                        When(name__icontains=search, then=2),
                        When(name_ru__icontains=search, then=2),
                        default=0,
                    )
                )
                .filter(relevance__gt=0)
                .order_by("-relevance")
                .first()
            )

            if not subcategory:
                return Product.objects.none()

        # 📂 SUBCATEGORY FLOW
        else:
            subcategory = SubCategory.objects.filter(
                slug=subcategory_slug
            ).first()

            if not subcategory:
                raise ValidationError({
                    "subcategory": "Invalid subcategory slug"
                })

        qs = qs.filter(category=subcategory)

        # 🧩 FILTER VALUES (AND logic)
        filters = params.get("filters")
        if filters:
            filter_ids = [int(f) for f in filters.split(",") if f.isdigit()]

            if filter_ids:
                qs = (
                    qs.filter(filters__id__in=filter_ids)
                    .annotate(
                        matched_filters=Count(
                            "filters",
                            filter=Q(filters__id__in=filter_ids),
                            distinct=True,
                        )
                    )
                    .filter(matched_filters=len(filter_ids))
                )

        # 💰 PRICE FILTER
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
                "subcategory": "This query param is required (category=<slug>)"
            })

        subcategory = SubCategory.objects.filter(
            slug=subcategory_slug
        ).first()
        category = subcategory.category

        if not category:
            raise ValidationError({
                "subcategory": "Invalid subcategory slug"
            })

        filters = (
            FilterType.objects
            .filter(category=category)
            .prefetch_related("filtervalue_set")
            .order_by("id")
        )

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


class CategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.all()


class SubCategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = SubCategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return SubCategory.objects.all()


class BannersListAPIView(ListAPIView):
    serializer_class = PromoBannerSerializer
    model = PromoBanner
    queryset = PromoBanner.objects.all()

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    FilterType,
    FilterValue,
    PromoBanner,
    Category,
    SubCategory,
    Product,
    ProductStatistic,
    ProductReview,
    ProductProperty,
    ProductImage,
    ProductDescriptionItem,
)


class FilterTypeSerializer(ModelSerializer):
    class Meta:
        model = FilterType
        fields = (
            "id",
            "name",
            "name_ru",
        )


class FilterValueSerializer(ModelSerializer):

    class Meta:
        model = FilterValue
        fields = (
            "id",
            "filter",
            "value",
            "value_ru",
        )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "name_ru",
            "slug",
            "image",
        )


class SubCategorySerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = (
            "id",
            "category",
            "name",
            "name_ru",
            "slug",
            "image",
        )


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
        )


class ProductPropertySerializer(ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = (
            "id",
            "name",
            "name_ru",
            "value",
            "value_ru",
        )


class ProductDescriptionItemSerializer(ModelSerializer):
    class Meta:
        model = ProductDescriptionItem
        fields = (
            "id",
            "text",
            "text_ru",
        )


class ProductStatisticSerializer(ModelSerializer):
    class Meta:
        model = ProductStatistic
        fields = (
            "views",
            "sold",
            "rating",
            "reviews_count",
        )


class ProductReviewSerializer(ModelSerializer):
    class Meta:
        model = ProductReview
        fields = (
            "id",
            "name",
            "email",
            "rating",
            "text",
            "created_at",
        )


class ProductSmallSerializer(ModelSerializer):
    category = SubCategorySerializer(read_only=True)
    statistics = ProductStatisticSerializer(read_only=True)
    image = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "name_ru",
            "slug",
            "price",
            "sale",
            "category",
            "image",
            "statistics",
            "vendor_code_public",
        )

    def get_image(self, obj):
        image = (
            ProductImage.objects
            .filter(product=obj)
            .values_list("image", flat=True)
            .first()
        )
        return image


class ProductBigSerializer(ModelSerializer):
    category = SubCategorySerializer(read_only=True)
    filters = FilterValueSerializer(many=True, read_only=True)
    statistics = ProductStatisticSerializer(read_only=True)

    images = ProductImageSerializer(
        source="productimage_set",
        many=True,
        read_only=True,
    )

    properties = ProductPropertySerializer(
        source="productproperty_set",
        many=True,
        read_only=True,
    )
    descriptions = ProductDescriptionItemSerializer(
        source="productdescriptionitem_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "name_ru",
            "slug",
            "price",
            "sale",
            "quantity",
            "description_en",
            "description_ru",
            "video",
            "category",
            "filters",
            "images",
            "properties",
            "descriptions",
            "statistics",
            "reviews",
            "created_at",
            "vendor_code_public",
        )


class FilterTypeWithValuesSerializer(ModelSerializer):
    values = FilterValueSerializer(
        source="filtervalue_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = FilterType
        fields = (
            "id",
            "name",
            "name_ru",
            "values",
        )


class PromoBannerSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = PromoBanner
        fields = (
            "id",
            "image",
            "image_mobile",
            "alt",
            "category",
        )

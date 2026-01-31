from django.contrib import admin
from .models import (
    Product,
    Category,
    SubCategory,
    ProductImage,
    ProductDescriptionItem,
    PromoBanner,
    FilterValue,
    FilterType,
    ProductStatistic,
    ProductReview,
    ProductProperty,
)


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductImage)
admin.site.register(ProductDescriptionItem)
admin.site.register(PromoBanner)
admin.site.register(FilterType)
admin.site.register(FilterValue)
admin.site.register(ProductStatistic)
admin.site.register(ProductProperty)
admin.site.register(ProductReview)

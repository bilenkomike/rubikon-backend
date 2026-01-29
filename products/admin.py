from django.contrib import admin
from .models import (
    Product,
    Category,
    SubCategory,
    ProductImage,
    ProductDescriptionItem,
    Banner,
    FilterValue,
    FilterType,
    ProductStatistic,
    ProductReview,
)


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductImage)
admin.site.register(ProductDescriptionItem)
admin.site.register(Banner)
admin.site.register(FilterType)
admin.site.register(FilterValue)
admin.site.register(ProductStatistic)

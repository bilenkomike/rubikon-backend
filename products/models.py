from django.db import models
from autoslug import AutoSlugField
from core.models.timestamped import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator


class FilterType(models.Model):
    """Filter name model."""
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    name_ru = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class FilterValue(models.Model):
    """Filter value to the filter name."""
    filter = models.ForeignKey(
        FilterType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    value = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    value_ru = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.value


class Banner(models.Model):
    """Banner model data structure."""
    image = models.ImageField(
        upload_to="banners/",
        null=False,
        blank=False,
    )
    alt = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.alt


class Category(models.Model):
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        editable=False
    )
    image = models.ImageField(
        upload_to="categories/",
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.slug


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        editable=False
    )

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=120)
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        editable=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    sale = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Discount percentage from 0 to 100"
    )
    video = models.FileField(
        upload_to="products/videos/",
        null=True,
        blank=True
    )
    filters = models.ManyToManyField(
        FilterValue,
        related_name="products",
        blank=True
    )

    def __str__(self):
        return self.name


class ProductDescriptionItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        max_length=300,
        null=False,
        blank=False,
    )
    text_ru = models.TextField(
        max_length=300,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.text


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to="products/images/",
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.product.name


class ProductStatistic(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="statistics"
    )
    views = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )
    reviews_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.product.name}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    name = models.CharField(
        max_length=120,
        help_text="Reviewer name"
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    text = models.TextField(
        max_length=1000
    )

    is_approved = models.BooleanField(
        default=False,
        help_text="Moderation flag"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.product.name} – {self.rating}★"


class ProductProperty(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    name_ru = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    value = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    value_ru = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    def __str__(self):
        return f"{self.name} - {self.value}"

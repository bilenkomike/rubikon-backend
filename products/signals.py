from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F

from orders.models import OrderItem
from .models import Product, ProductStatistic, ProductReview


@receiver(post_save, sender=Product)
def create_product_stats(sender, instance, created, **kwargs):
    if created:
        ProductStatistic.objects.create(product=instance)


@receiver(post_save, sender=ProductReview)
def update_product_rating(sender, instance, **kwargs):
    stats = ProductStatistic.objects.filter(
        product=instance.product
    ).first()

    if not stats:
        return

    agg = ProductReview.objects.filter(
        product=instance.product
    ).aggregate(
        avg=Avg("rating")
    )

    stats.reviews_count = ProductReview.objects.filter(
        product=instance.product
    ).count()
    stats.rating = agg["avg"] or 0
    stats.save(update_fields=["reviews_count", "rating"])


@receiver(post_save, sender=OrderItem)
def update_product_sales(sender, instance, created, **kwargs):
    if not created:
        return

    ProductStatistic.objects.filter(
        product=instance.product
    ).update(
        sold=F("sold") + instance.quantity,
    )

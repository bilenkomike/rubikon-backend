from django.db import models
from users.models import User
from products.models import Product
from core.models.timestamped import TimeStampedModel
from products.models import FilterValue


class Wishlist(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class OrderStatus(models.TextChoices):
    DRAFT = "draft"
    PLACED = "placed"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(TimeStampedModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32,
        choices=OrderStatus.choices,
        default=OrderStatus.PLACED
    )

    total = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    filter_values = models.ManyToManyField(
        FilterValue,
        blank=True,
        related_name="order_items",
        help_text="Selected filter values",
    )

    def get_total(self):
        return self.price * self.quantity

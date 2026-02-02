from orders.models import Order, OrderItem, OrderStatus
from orders.models import CartItem
from django.db import transaction
from decimal import Decimal


@transaction.atomic
def create_order_from_cart(user, note=""):
    cart_items = (
        CartItem.objects
        .select_related("product")
        .prefetch_related("filter_values")
        .filter(user=user)
    )

    if not cart_items.exists():
        raise ValueError("Cart is empty")

    total = Decimal("0.00")

    order = Order.objects.create(
        buyer=user,
        status=OrderStatus.PLACED,
        total=0,
        note=note,
    )

    for item in cart_items:
        product = item.product
        price = product.price
        sale = product.sale or 0

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=item.quantity,
            sale=sale,
        )

        if sale:
            price = price - (price * Decimal(sale) / Decimal(100))
        line_total = price * item.quantity
        total += line_total

        if item.filter_values.exists():
            order_item.filter_values.set(item.filter_values.all())
    print(total)
    order.total = total
    order.save(update_fields=["total"])

    cart_items.delete()

    return order

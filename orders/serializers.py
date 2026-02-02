from rest_framework.serializers import ModelSerializer, SerializerMethodField
from orders.models import CartItem
from products.serializers import ProductSmallSerializer
from orders.models import Order, OrderItem


class CartItemSerializer(ModelSerializer):
    product = ProductSmallSerializer(read_only=True)
    filter_values = SerializerMethodField()
    total = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product",
            "quantity",
            "filter_values",
            "total",
        )

    def get_total(self, obj):
        price = obj.product.price
        if obj.product.sale:
            price = price - (price * obj.product.sale / 100)
        total = price * obj.quantity
        return total

    def get_filter_values(self, obj):
        return [
            {
                "id": fv.id,
                "name": fv.value,
                "name_ru": fv.value_ru,
            }
            for fv in obj.filter_values.all()
        ]


class OrderItemSerializer(ModelSerializer):
    product_title = SerializerMethodField()
    filter_values = SerializerMethodField()
    total = SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_title",
            "price",
            "quantity",
            "sale",
            "filter_values",
            "total",
        )

    def get_product_title(self, obj):
        return obj.product.name

    def get_total(self, obj):
        return obj.get_total()

    def get_filter_values(self, obj):
        return [
            {
                "id": fv.id,
                "name": fv.value,
                "name_ru": fv.value_ru,
            }
            for fv in obj.filter_values.all()
        ]


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total",
            "note",
            "created_at",
            "items",
        )

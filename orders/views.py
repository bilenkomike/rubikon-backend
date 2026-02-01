from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem, OrderStatus, CartItem
from .serializers import OrderSerializer

from .models import CartItem
from products.models import Product, FilterValue
from .serializers import CartItemSerializer


class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = (
            CartItem.objects
            .filter(user=request.user)
            .select_related("product")
            .prefetch_related("filter_values")
        )
        return Response(CartItemSerializer(items, many=True).data)


class CartAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        filter_ids = request.data.get("filter_values", [])

        product = Product.objects.get(id=product_id)
        filters = FilterValue.objects.filter(id__in=filter_ids)

        # check existing cart item with same filters
        existing = (
            CartItem.objects
            .filter(user=request.user, product=product)
            .prefetch_related("filter_values")
        )

        for item in existing:
            if set(item.filter_values.all()) == set(filters):
                item.quantity += quantity
                item.save()
                return Response(CartItemSerializer(item).data)

        item = CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
        )
        item.filter_values.set(filters)

        return Response(
            CartItemSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )


class CartUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        quantity = int(request.data.get("quantity"))

        item = CartItem.objects.get(id=pk, user=request.user)

        if quantity <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        item.quantity = quantity
        item.save()

        return Response(CartItemSerializer(item).data)


class CartRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        CartItem.objects.filter(id=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = (
            CartItem.objects
            .filter(user=request.user)
            .select_related("product")
            .prefetch_related("filter_values")
        )

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            order = Order.objects.create(
                buyer=request.user,
                status=OrderStatus.PLACED,
                total=0,
                note=request.data.get("note", ""),
            )

            total = 0

            for item in cart_items:
                price = item.product.price
                sale = item.product.sale or 0
                discounted = price * (100 - sale) / 100

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=price,
                    quantity=item.quantity,
                    sale=sale,
                ).filter_values.set(item.filter_values.all())

                total += discounted * item.quantity

            order.total = total
            order.save()

            cart_items.delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(buyer=request.user)
            .prefetch_related("items__filter_values")
            .order_by("-created_at")
        )
        return Response(OrderSerializer(orders, many=True).data)


class OrderRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.prefetch_related(
            "items__filter_values"
        ).get(id=pk, buyer=request.user)

        return Response(OrderSerializer(order).data)
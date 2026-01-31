from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from orders.models import Wishlist
from products.models import Product


from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer, WishlistSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class MeAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {"detail": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.save()

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


class WishlistAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data, request.data.get("product_id"))
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"detail": "Product ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product = Product.objects.get(id=product_id)
        Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )

        return Response(
            {"detail": "Added to wishlist"},
            status=status.HTTP_201_CREATED,
        )


class WishlistListAPIView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class WishlistRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        Wishlist.objects.filter(
            user=request.user,
            product_id=product_id,
        ).delete()

        return Response(
            {"detail": "Removed from wishlist"},
            status=status.HTTP_200_OK,
        )
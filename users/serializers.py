from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    ValidationError,
    CharField,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from orders.models import Wishlist

User = get_user_model()


from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(Serializer):
    old_password = CharField(write_only=True)
    new_password = CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )
        read_only_fields = ("id",)


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # access to authenticated user
        user = self.user

        # add user info to response body
        data["user"] = ProfileSerializer(user, many=False).data

        return data


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)
    password_confirm = CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({
                "password": "Passwords do not match"
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "id",
            "product",
        )

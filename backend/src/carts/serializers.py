from courses.serializers import CartCourseSerializer

from rest_framework import serializers

from carts.models import Cart, Wishlist


class CartSerializer(serializers.ModelSerializer):
    courses = CartCourseSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "courses",
            "subtotal",
            "total",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    courses = CartCourseSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = [
            "courses",
        ]

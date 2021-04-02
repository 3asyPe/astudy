from courses.serializers import CartCourseSerializer

from rest_framework import serializers

from carts.models import Cart, Wishlist, SavedForLater


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


class CartOnlyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
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


class SavedForLaterSerializer(serializers.ModelSerializer):
    courses = CartCourseSerializer(many=True)
     
    class Meta:
        model = SavedForLater
        fields = [
            "id",
            "courses",
        ]

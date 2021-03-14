from courses.serializers import CartCourseSerializer

from rest_framework import serializers

from .models import Cart


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

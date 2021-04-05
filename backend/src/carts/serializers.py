from courses.serializers import CartCourseSerializer

from rest_framework import serializers

from carts.models import Cart, Wishlist, SavedForLater
from courses.services import CourseSelector
from discounts.services import DiscountSelector
from discounts.serializers import AppliedCouponSerializer


class CartSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    applied_coupons = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "courses",
            "applied_coupons",
            "subtotal",
            "total",
        ]

    def get_courses(self, obj):
        courses = CourseSelector.get_courses_by_cart(cart=obj)
        return CartCourseSerializer(instance=courses, many=True, context={"cart": obj}).data

    def get_applied_coupons(self, obj):
        coupons = DiscountSelector.get_applied_coupons_for_cart(cart=obj)
        serializer = AppliedCouponSerializer(instance=coupons, many=True)
        return serializer.data


class CartOnlyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "subtotal",
            "total",
        ]


class CartDiscountsInfoSerializer(serializers.ModelSerializer):
    discounts = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "discounts",
            "subtotal",
            "total",
        ]

    def get_discounts(self, obj):
        discounts = DiscountSelector.get_discounts_for_cart(cart=obj)
        return [discount.serialize() for discount in discounts if discount is not None]


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

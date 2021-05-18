import logging

from courses.serializers import CartCourseSerializer

from rest_framework import serializers

from carts.models import Cart, Wishlist, SavedForLater
from courses.services import CourseSelector
from discounts.services import DiscountSelector
from discounts.serializers import AppliedCouponSerializer


logger = logging.getLogger(__name__)


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
    cart_discounts = serializers.SerializerMethodField()
    wishlist_discounts = serializers.SerializerMethodField()
    saved_for_later_discounts = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "cart_discounts",
            "wishlist_discounts",
            "saved_for_later_discounts",
            "subtotal",
            "total",
        ]

    def get_cart_discounts(self, obj):
        discounts = DiscountSelector.get_discounts_for_cart(cart=obj)
        return [discount.serialize() for discount in discounts if discount is not None]

    def get_wishlist_discounts(self, obj):
        wishlist = self.context.get("wishlist")
        if wishlist is None:
            return None
        discounts = DiscountSelector.get_discounts_for_wishlist(cart=obj, wishlist=wishlist)
        return [discount.serialize() for discount in discounts if discount is not None]

    def get_saved_for_later_discounts(self, obj):
        saved_for_later = self.context.get('saved_for_later')
        if saved_for_later is None:
            return None
        discounts = DiscountSelector.get_discounts_for_saved_for_later(cart=obj, saved_for_later=saved_for_later)
        return [discount.serialize() for discount in discounts if discount is not None]


class WishlistSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            "courses",
        ]

    def get_courses(self, obj):
        cart = self.context["cart"]
        courses = CourseSelector.get_courses_by_wishlist(wishlist=obj)
        return CartCourseSerializer(instance=courses, many=True, context={"cart": cart}).data


class SavedForLaterSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
     
    class Meta:
        model = SavedForLater
        fields = [
            "id",
            "courses",
        ]

    def get_courses(self, obj):
        cart = self.context["cart"]
        courses = CourseSelector.get_courses_by_saved_for_later(saved_for_later=obj)
        return CartCourseSerializer(instance=courses, many=True, context={"cart": cart}).data

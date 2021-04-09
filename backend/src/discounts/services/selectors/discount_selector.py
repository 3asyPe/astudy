import logging

from typing import List, Optional

from django.db.models import QuerySet

from carts.models import Cart, SavedForLater, Wishlist
from courses.models import Course
from courses.services import CourseSelector
from discounts.models import AppliedCoupon, Coupon
from discounts.services import CourseDiscount


logger = logging.getLogger(__name__)


class DiscountSelector:
    @classmethod
    def get_discount_for_course_or_nothing(cls, course: Course, cart: Cart) -> Optional[CourseDiscount]:
        return CourseDiscount.get_or_nothing(cart=cart, course=course)

    @classmethod
    def get_discounts_for_cart(cls, cart: Cart) -> List[CourseDiscount]:
        courses = CourseSelector.get_courses_by_cart(cart=cart)
        discounts = [CourseDiscount.get_or_nothing(course=course, cart=cart) for course in courses.iterator()]
        return discounts

    @classmethod
    def get_discounts_for_wishlist(cls, cart: Cart, wishlist: Wishlist) -> List[CourseDiscount]:
        courses = CourseSelector.get_courses_by_wishlist(wishlist=wishlist)
        discounts = [CourseDiscount.get_or_nothing(course=course, cart=cart) for course in courses.iterator()]
        logger.debug(f"Wishlist courses - {courses}")
        logger.debug(f"Wishlist discounts - {discounts}")
        return discounts

    @classmethod
    def get_discounts_for_saved_for_later(cls, cart: Cart, saved_for_later: SavedForLater) -> List[SavedForLater]:
        courses = CourseSelector.get_courses_by_saved_for_later(saved_for_later=saved_for_later)
        discounts = [CourseDiscount.get_or_nothing(course=course, cart=cart) for course in courses.iterator()]
        logger.debug(f"Saved for later courses - {courses}")
        logger.debug(f"Saved for later discounts - {discounts}")
        return discounts

    @classmethod
    def get_applied_coupons_for_cart(cls, cart: Cart) -> List[AppliedCoupon]:
        active_coupons = []
        for coupon in AppliedCoupon.objects.active_coupons().filter(cart=cart):
            if coupon.is_active:
                active_coupons.append(coupon)
        return active_coupons

    @classmethod
    def get_applied_coupons_by_coupon(cls, coupon: Coupon) -> QuerySet(AppliedCoupon):
        return AppliedCoupon.objects.filter(coupon=coupon, active=True)

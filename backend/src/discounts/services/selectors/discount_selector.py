from typing import List, Optional

from django.db.models import QuerySet

from carts.models import Cart
from courses.models import Course
from courses.services import CourseSelector
from discounts.models import AppliedCoupon, Coupon
from discounts.services import CourseDiscount


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
    def get_applied_coupons_for_cart(cls, cart: Cart) -> List[AppliedCoupon]:
        active_coupons = []
        for coupon in AppliedCoupon.objects.active_coupons():
            if coupon.is_active:
                active_coupons.append(coupon)
        return active_coupons

    @classmethod
    def get_applied_coupons_by_coupon(cls, coupon: Coupon) -> QuerySet(AppliedCoupon):
        return AppliedCoupon.objects.filter(coupon=coupon, active=True)

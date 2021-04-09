import logging

from decimal import Decimal
from typing import Optional, Union

from app.errors import DiscountDoesNotExistError
from carts.models import Cart, SavedForLater, Wishlist
from courses.models import Course
from discounts.models import AppliedCoupon


logger = logging.getLogger(__name__)


class CourseDiscount:
    def __init__(
        self,
        course: Course,
        cart: Cart,
    ):
        self.course = course
        self.cart = cart
        self.old_price = self.course.price
        self.new_price = self.old_price
        self.applied_coupon = None

        self.apply_coupons()
        self.count_price()

    def serialize(self):
        return {
            "course_slug": self.course.slug,
            "new_price": str(self.new_price),
            "applied_coupon": self.applied_coupon.code,
        }

    def apply_coupons(self) -> None:
        coupons = AppliedCoupon.objects.filter(cart=self.cart, coupon__applicable_to__in=[self.course], active=True)
        logger.debug(f"course-{self.course}")
        logger.debug(f"coupons-{coupons}")
        max_discount = 0
        max_discount_coupon = None
        for coupon in coupons:
            if coupon.is_active and coupon.discount > max_discount:
                max_discount_coupon = coupon 
                max_discount = coupon.discount
        logger.debug(f"applied - {max_discount_coupon}")
        self.applied_coupon = max_discount_coupon
    
    def count_price(self) -> None:
        if self.applied_coupon:
            self.new_price = round(self.old_price * Decimal((1 - self.applied_coupon.discount / 100)), 2)
        else:
            self.new_price = self.old_price

    @classmethod
    def get_or_nothing(cls, course: Course, cart: Cart):
        logger.debug(f"COURSE-{course}")
        logger.debug(f"CART-{cart}")
        try:
            return cls.get(course=course, cart=cart)
        except DiscountDoesNotExistError:
            return None

    @classmethod
    def get(cls, course: Course, cart: Cart):
        instance = cls(course=course, cart=cart)
        if instance.applied_coupon is None:
            raise DiscountDoesNotExistError()
        return instance

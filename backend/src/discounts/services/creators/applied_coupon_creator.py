from typing import List, Optional

from app.errors import ValidationError
from carts.models import Cart
from courses.models import Course
from discounts.models import AppliedCoupon, Coupon
from discounts.utils import DiscountErrorMessages


class AppliedCouponCreator:
    def __init__(
        self, 
        code: str,
        cart: Cart,
    ):
        self.code = code
        self.cart = cart
        self.coupon = self._get_coupon()

    def __call__(self) -> AppliedCoupon:
        if self.allowed_to_create():
            return self.create()
        raise ValidationError(DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value)

    def create(self) -> AppliedCoupon:
        return AppliedCoupon.objects.create(
            coupon=self.coupon,
            cart=self.cart,
        )

    def allowed_to_create(self) -> bool:
        if self.coupon is None or not self.coupon.is_active:
            return False

        if AppliedCoupon.objects.filter(coupon__code=self.code, cart=self.cart).exists():
            return False

        return True

    def _get_coupon(self) -> Optional[Coupon]:
        qs = Coupon.objects.filter(code=self.code)
        if qs.exists():
            return qs.first()
        return None

from typing import Optional

from carts.models import Cart
from discounts.models import AppliedCoupon
from discounts.services import AppliedCouponCreator


class CouponToolkit:
    @classmethod
    def apply_coupon(cls, code: str, cart: Cart) -> Optional[Cart]:
        applied_coupon = AppliedCouponCreator(code=code, cart=cart)()
        cart.update_totals()
        return applied_coupon

    @classmethod
    def remove_applied_coupon(cls, code: str, cart: Cart) -> None:
        qs = AppliedCoupon.objects.filter(coupon__code=code, cart=cart)
        if qs.exists():
            applied_coupon = qs.first()
            applied_coupon.delete()
            cart.update_totals()

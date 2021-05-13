import pytest

from app.errors import ValidationError
from discounts.services import AppliedCouponCreator
from discounts.utils import DiscountErrorMessages


pytestmark = [pytest.mark.django_db]


def test_create_valid_applied_coupon(coupon, cart):
    applied_coupon = AppliedCouponCreator(
        code=coupon.code,
        cart=cart
    )()

    assert applied_coupon.coupon == coupon
    assert applied_coupon.cart == cart
    assert applied_coupon.active == True


def test_create_applied_coupon_with_wrong_code(cart):
    with pytest.raises(ValidationError) as exc:
        applied_coupon = AppliedCouponCreator(code="WRONGCODE", cart=cart)()

    assert str(exc.value) == DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value


def test_create_applied_coupon_with_inactive_code(coupon, cart):
    coupon.active = False
    coupon.save()

    with pytest.raises(ValidationError) as exc:
        applied_coupon = AppliedCouponCreator(code=coupon.code, cart=cart)()

    assert str(exc.value) == DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value


def test_create_already_existing_applied_coupon(applied_coupon, cart):
    with pytest.raises(ValidationError) as exc:
        applied_coupon = AppliedCouponCreator(code=applied_coupon.coupon.code, cart=cart)()

    assert str(exc.value) == DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value

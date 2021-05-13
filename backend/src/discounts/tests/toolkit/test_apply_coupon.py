import pytest

from decimal import Decimal

from app.errors import ValidationError
from discounts.services import CouponToolkit
from discounts.utils import DiscountErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, course_factory):
    cart.courses.add(course_factory())
    cart.courses.add(course_factory())
    return cart


def test_applying_valid_coupon(coupon, cart):
    coupon.applicable_to.add(cart.courses.first())
    applied_coupon = CouponToolkit.apply_coupon(code=coupon.code, cart=cart)

    assert applied_coupon.coupon == coupon
    assert applied_coupon.cart == cart
    assert applied_coupon.active == True

    assert cart.subtotal == cart.courses.first().price + cart.courses.last().price
    assert cart.total == round(cart.courses.first().price * Decimal('0.9'), 2) + cart.courses.last().price


def test_applying_invalid_coupon(cart):
    with pytest.raises(ValidationError) as exc:
        CouponToolkit.apply_coupon(code="WRONGCODE", cart=cart)
    
    assert str(exc.value) == DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value
    assert cart.total == cart.subtotal == cart.courses.first().price + cart.courses.last().price

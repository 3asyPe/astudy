import pytest

from decimal import Decimal

from discounts.services import CouponToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, course_factory):
    cart.courses.add(course_factory())
    cart.courses.add(course_factory())
    return cart


@pytest.fixture
def applied_coupon(applied_coupon, cart):
    applied_coupon.coupon.applicable_to.add(cart.courses.first())
    cart.update_totals()
    assert cart.subtotal == cart.courses.first().price + cart.courses.last().price
    assert cart.total == round(cart.courses.first().price * Decimal('0.9'), 2) + cart.courses.last().price
    return applied_coupon


def test_removing_applied_coupon(applied_coupon, cart):
    CouponToolkit.remove_applied_coupon(applied_coupon.coupon.code, cart)

    assert cart.total == cart.subtotal == cart.courses.first().price + cart.courses.last().price


def test_removing_wrong_coupon(applied_coupon, cart):
    CouponToolkit.remove_applied_coupon("WRONGCODE", cart)

    assert cart.total == round(cart.courses.first().price * Decimal('0.9'), 2) + cart.courses.last().price

import pytest

from decimal import Decimal

from discounts.services import CourseDiscount


pytestmark = [pytest.mark.django_db]


def test_create_course_discount(cart):
    course = cart.courses.last()
    coupon = cart.applied_coupons.last()
    discount = CourseDiscount.get(course=course, cart=cart)

    assert discount.course == course
    assert discount.cart == cart
    assert discount.old_price == course.price
    assert discount.new_price == round(course.price * Decimal('0.8'), 2)
    assert discount.applied_coupon == coupon


def test_create_course_discount_without_applied_coupons(cart):
    course = cart.courses.first()
    cart.applied_coupons.first().delete()
    discount = CourseDiscount.get_or_nothing(course, cart)

    assert discount is None

import pytest

from decimal import Decimal

from discounts.services import CourseDiscount


pytestmark = [pytest.mark.django_db]


def test_course_discount_serialization(cart):
    course = cart.courses.first()
    coupon = cart.applied_coupons.first()

    discount = CourseDiscount.get(course=course, cart=cart)
    serialized = discount.serialize()

    assert serialized["course_slug"] == course.slug
    assert serialized["new_price"] == str(round(course.price * Decimal('0.9'), 2))
    assert serialized["applied_coupon"] == coupon.code

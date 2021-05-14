import pytest

from decimal import Decimal

from discounts.services import CourseDiscount


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("percent", [10, 32, 98])
def test_course_discount_price_counting(cart, percent):
    coupon = cart.applied_coupons.first().coupon
    coupon.discount = percent
    coupon.save()

    course = cart.courses.first()
    
    discount = CourseDiscount.get(course=course, cart=cart)

    assert discount.new_price == round(course.price * Decimal((1 - percent / 100)), 2)
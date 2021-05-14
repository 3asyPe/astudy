import pytest

from decimal import Decimal

from discounts.services import CourseDiscount


pytestmark = [pytest.mark.django_db]


def test_course_discounts_for_cart_with_coupon_for_one_course(cart):
    course1 = cart.courses.first()
    course2 = cart.courses.last()

    coupon = cart.applied_coupons.last()
    cart.applied_coupons.first().delete()

    discount1 = CourseDiscount.get_or_nothing(course=course1, cart=cart)
    discount2 = CourseDiscount.get_or_nothing(course=course2, cart=cart)

    assert discount1 is None
    assert discount2.new_price == round(course2.price * Decimal('0.8'), 2)
    assert discount2.applied_coupon == coupon


def test_course_discounts_for_cart_with_same_coupon_for_both_courses(cart):
    course1 = cart.courses.first()
    course2 = cart.courses.last()

    coupon = cart.applied_coupons.first()
    cart.applied_coupons.last().delete()

    discount1 = CourseDiscount.get_or_nothing(course=course1, cart=cart)
    discount2 = CourseDiscount.get_or_nothing(course=course2, cart=cart)

    assert discount1.new_price == round(course1.price * Decimal('0.9'), 2)
    assert discount1.applied_coupon == coupon
    assert discount2.new_price == round(course2.price * Decimal('0.9'), 2)
    assert discount2.applied_coupon == coupon


def test_course_discounts_for_cart_with_different_coupons(cart):
    course1 = cart.courses.first()
    course2 = cart.courses.last()

    coupon1 = cart.applied_coupons.first()
    coupon2 = cart.applied_coupons.last()

    discount1 = CourseDiscount.get_or_nothing(course=course1, cart=cart)
    discount2 = CourseDiscount.get_or_nothing(course=course2, cart=cart)

    assert discount1.new_price == round(course1.price * Decimal('0.9'), 2)
    assert discount1.applied_coupon == coupon1
    assert discount2.new_price == round(course2.price * Decimal('0.8'), 2)
    assert discount2.applied_coupon == coupon2

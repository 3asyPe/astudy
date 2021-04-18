import pytest

from decimal import Decimal

from carts.services import CartToolkit
from discounts.services import CourseDiscount


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart_with_one_course_with_zero_totals(course_factory, cart):
    cart.courses.add(course_factory())
    cart.total = 0
    cart.subtotal = 0
    cart.save()
    return cart


@pytest.fixture
def cart_with_two_courses_with_zero_totals(course_factory, cart):
    cart.courses.add(course_factory())
    cart.courses.add(course_factory())
    cart.total = 0
    cart.subtotal = 0
    cart.save()
    return cart


@pytest.fixture
def discount(cart_with_one_course_with_zero_totals, mocker):
    cart = cart_with_one_course_with_zero_totals
    course = cart.courses.first()
    discount = mocker.patch("discounts.services.CourseDiscount")
    discount.cart = cart
    discount.course = course
    discount.new_price = round(course.price * Decimal((1 - 10 / 100)), 2)
    return discount


def test_updating_cart_totals_for_empty_cart(cart):
    CartToolkit.update_cart_totals(cart=cart)

    cart.refresh_from_db()

    assert cart.subtotal == cart.total == 0


def test_updating_cart_totals_without_discounts(cart_with_one_course_with_zero_totals, course_factory):
    cart = cart_with_one_course_with_zero_totals
    CartToolkit.update_cart_totals(cart=cart)

    cart.refresh_from_db()

    assert cart.subtotal == cart.total == cart.courses.first().price


def test_updating_cart_totals_with_discount(mocker, cart_with_one_course_with_zero_totals, discount):
    cart = cart_with_one_course_with_zero_totals
    mocker.patch(
        "discounts.services.DiscountSelector.get_discount_for_course_or_nothing",
        return_value=discount
    )
    CartToolkit.update_cart_totals(cart=cart)

    cart.refresh_from_db()

    assert cart.subtotal == cart.courses.first().price
    assert cart.total == discount.new_price


def test_updating_cart_totals_with_multiple_courses_without_discounts(cart_with_two_courses_with_zero_totals):
    cart = cart_with_two_courses_with_zero_totals
    CartToolkit.update_cart_totals(cart=cart)

    cart.refresh_from_db()

    total = cart.courses.first().price + cart.courses.last().price
    assert cart.subtotal == cart.total == total

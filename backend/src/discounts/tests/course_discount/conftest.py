import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def small_coupon(mixer):
    return mixer.blend("discounts.Coupon", discount=10)


@pytest.fixture
def big_coupon(mixer):
    return mixer.blend("discounts.Coupon", discount=20)


@pytest.fixture
def cart(mixer, small_coupon, big_coupon, cart, course_factory):
    mixer.blend("discounts.AppliedCoupon", coupon=small_coupon, cart=cart)
    mixer.blend("discounts.AppliedCoupon", coupon=big_coupon, cart=cart)
    
    course1 = course_factory()
    course2 = course_factory()

    cart.courses.add(course1)
    cart.courses.add(course2)

    small_coupon.applicable_to.add(course1)
    small_coupon.applicable_to.add(course2)
    big_coupon.applicable_to.add(course2)

    return cart
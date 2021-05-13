import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def coupon(mixer, user):
    return mixer.blend(
        "discounts.Coupon",
        creator=user,
        discount=10,
    )


@pytest.fixture
def applied_coupon(mixer, coupon, cart):
    return mixer.blend(
        "discounts.AppliedCoupon",
        coupon=coupon,
        cart=cart
    )
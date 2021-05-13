import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def coupon(mixer, user):
    return mixer.blend(
        "discounts.Coupon",
        creator=user,
    )
import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order(mixer, billing_profile, cart):
    return mixer.blend(
        "orders.Order",
        billing_profile=billing_profile,
        cart=cart,
    )
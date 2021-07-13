import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order(mixer, billing_profile, cart, payment_method):
    return mixer.blend(
        "orders.Order",
        billing_profile=billing_profile,
        cart=cart,
        payment_method=payment_method,
    )


@pytest.fixture
def payment_method(mixer):
    return mixer.blend(
        "orders.PaymentMethod",
        type="CARD",
    )

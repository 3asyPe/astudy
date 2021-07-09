import pytest

from orders.models import Order


pytestmark = [pytest.mark.django_db]


def test_setting_order_id_after_creation(mixer, billing_profile, cart):
    order = mixer.blend(
        "orders.Order",
        order_id=None,
        billing_profile=billing_profile, 
        cart=cart,
    )

    assert order.order_id


def test_setting_order_id_after_deleting_it(order):
    order.order_id = ""
    order.save()

    assert order.order_id

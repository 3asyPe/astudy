import pytest

from orders.models import Order


pytestmark = [pytest.mark.django_db]


def test_setting_order_id_after_creation(mixer, billing_profile, cart, payment_method):
    order = Order.objects.create(
        billing_profile=billing_profile, 
        cart=cart,
        payment_method=payment_method,
    )

    assert order.order_id


def test_setting_order_id_after_deleting_it(order):
    order.order_id = ""
    order.save()

    assert order.order_id

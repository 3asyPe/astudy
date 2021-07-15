import pytest

from app.errors import ValidationError
from orders.models import Order
from orders.services import OrderCreator
from orders.utils import OrderErorrMessages


pytestmark = [pytest.mark.django_db]


def test_order_creation(billing_profile, cart_with_course, payment_method):
    order = OrderCreator(
        billing_profile=billing_profile,
        cart=cart_with_course,
        payment_method=payment_method,
    )()

    assert order.order_id
    assert order.billing_profile == billing_profile
    assert order.cart == cart_with_course
    assert order.total == cart_with_course.total
    assert order.payment_method == payment_method
    assert order.paid == False
    assert order.shipped == False


def test_order_creation_with_empty_cart(billing_profile, cart, payment_method):
    with pytest.raises(ValidationError) as exc:
        order = OrderCreator(
            billing_profile=billing_profile,
            cart=cart,
            payment_method=payment_method
        )()

    assert str(exc.value) == OrderErorrMessages.EMPTY_CART_ERROR.value

import pytest

from orders.services import OrderToolkit


pytestmark = [pytest.mark.django_db]


def test_order_closing(mocker, order):
    deactivate_cart = mocker.patch("carts.models.Cart.deactivate")
    
    OrderToolkit.close_order(order)

    deactivate_cart.assert_called_once()

import pytest

from orders.services import OrderToolkit


pytestmark = [pytest.mark.django_db]


def test_charging_for_order(mocker, order, charge):
    charge_creator = mocker.patch("orders.services.ChargeCreator.__call__", return_value=charge)

    created_charge = OrderToolkit.charge_for_order(order)
    
    assert created_charge == charge
    charge_creator.assert_called_once()

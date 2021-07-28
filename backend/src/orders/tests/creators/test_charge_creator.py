import pytest

from app.errors import ValidationError
from app.integrations.stripe.errors import NotChargedStripeError
from orders.services import ChargeCreator
from orders.utils import ChargeErrorMessages


pytestmark = [pytest.mark.django_db]


def test_charge_creation(mocker, order, charge_stripe_response):
    mocker.patch(
        "app.integrations.stripe.AppStripe.create_charge", 
        return_value=charge_stripe_response
    )

    charge = ChargeCreator(order)()

    assert charge.order == order
    assert charge.billing_profile == order.billing_profile
    assert charge.payment_method == order.payment_method
    assert charge.stripe_id == charge_stripe_response["id"]
    assert charge.amount == order.total


def test_charge_creation_with_error_response(mocker, order, charge_stripe_error_response):
    mocker.patch(
        "app.integrations.stripe.AppStripe.create_charge", 
        return_value=charge_stripe_error_response
    )

    with pytest.raises(NotChargedStripeError):
        charge = ChargeCreator(order)()


def test_charge_creation_with_too_small_amount(mocker, order):
    order.total = 0.1
    order.save()

    with pytest.raises(ValidationError) as exc:
        charge = ChargeCreator(order)()
    
    assert str(exc.value) == ChargeErrorMessages.TOO_SMALL_AMOUNT_ERROR.value

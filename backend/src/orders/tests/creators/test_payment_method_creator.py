import pytest

from app.errors import ValidationError
from orders.services import PaymentMethodCreator
from orders.utils import PaymentMethodErrorMessages


pytestmark = [pytest.mark.django_db]


def test_payment_method_creation(mocker, settings):
    settings.STRIPE_API_TURNED_ON = True
    validate_token = mocker.patch("app.integrations.stripe.AppStripe.validate_token", return_value=True)

    payment_method = PaymentMethodCreator(
        type="CARD",
        stripe_token="tok_test",
    )()

    assert payment_method.type == "CARD"
    assert payment_method.stripe_token == "tok_test"
    assert not payment_method.card


def test_payment_method_creation_with_wrong_type():
    with pytest.raises(ValidationError) as exc:
        payment_method = PaymentMethodCreator(
            type="RANDOMMETHOD",
            stripe_token="tok_test",
        )()
    
    assert str(exc.value) == PaymentMethodErrorMessages.UNSUPPORTED_PAYMENT_METHOD_TYPE_ERROR.value


@pytest.mark.parametrize("token", ["somerandomstring", "tok_test"])
def test_payment_method_creation_with_wrong_stripe_id(token, mocker, settings):
    settings.STRIPE_API_TURNED_ON = True
    validate_token = mocker.patch("app.integrations.stripe.AppStripe.validate_token", return_value=False)

    with pytest.raises(ValidationError) as exc:
        payment_method = PaymentMethodCreator(
            type="CARD",
            stripe_token="somerandomstring",
        )()
    
    assert str(exc.value) == PaymentMethodErrorMessages.WRONG_STRIPE_TOKEN_ERROR.value

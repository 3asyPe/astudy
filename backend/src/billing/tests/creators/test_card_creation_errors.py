import pytest

from app.errors import ValidationError
from app.integrations.stripe.errors import StripeResponseFieldError
from app.integrations.stripe.utils import StripeErrorMessages
from billing.services import CardCreator
from billing.utils import CardErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("field", ["id", "brand", "last4"])
def test_card_creation_without_necessary_information(mocker, field, billing_profile, stripe_token, stripe_response):
    stripe_response.pop(field)

    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)

    with pytest.raises(StripeResponseFieldError):
        card = CardCreator(billing_profile=billing_profile, stripe_token=stripe_token)()


@pytest.mark.parametrize(["field", "value"], [
    ("id", "ba_1JCfc92eZvKYlo2CHTuR7XB7"),
    ("brand", ""),
    ("last4", "42424")
])
def test_card_creation_with_wrong_necessary_information(
    mocker, 
    field, 
    value, 
    billing_profile, 
    stripe_token, 
    stripe_response
):
    stripe_response[field] = value

    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)

    with pytest.raises(ValidationError) as exc:
        card = CardCreator(billing_profile=billing_profile, stripe_token=stripe_token)()

    if field == "id":
        assert str(exc.value) == CardErrorMessages.WRONG_CARD_STRIPE_ID_ERROR.value
    elif field == "brand":
        assert str(exc.value) == CardErrorMessages.WRONG_CARD_BRAND_ERROR.value
    else:
        assert str(exc.value) == CardErrorMessages.WRONG_CARD_LAST4_ERROR.value

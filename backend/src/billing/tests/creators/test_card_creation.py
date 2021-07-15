import json
import pytest

from billing.services import CardCreator


pytestmark = [pytest.mark.django_db]


def test_full_card_creation(mocker, billing_profile, stripe_token, stripe_response):
    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)
    set_as_default = mocker.patch("billing.models.Card.set_as_default")

    card = CardCreator(
        billing_profile=billing_profile, 
        stripe_token=stripe_token, 
        default=True,
    )()

    assert card.billing_profile == billing_profile
    assert card.stripe_id == "card_1JD9PPAGKJR9v1iNUvmLh76d"
    assert card.brand == "Visa"
    assert card.country == "US"
    assert card.postal_code == "242424"
    assert card.exp_month == 4
    assert card.exp_year == 2024
    assert card.last4 == "4242"

    set_as_default.assert_called_once()


def test_card_creation_with_partial_information(mocker, billing_profile, stripe_token, stripe_response):
    stripe_response.pop("address_zip")
    stripe_response.pop("exp_month")
    stripe_response.pop("exp_year")
    stripe_response.pop("country")

    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)

    card = CardCreator(billing_profile=billing_profile, stripe_token=stripe_token)()

    assert card.billing_profile == billing_profile
    assert card.stripe_id == "card_1JD9PPAGKJR9v1iNUvmLh76d"
    assert card.brand == "Visa"
    assert card.last4 == "4242"
    assert not card.country
    assert not card.postal_code
    assert not card.exp_month
    assert not card.exp_year

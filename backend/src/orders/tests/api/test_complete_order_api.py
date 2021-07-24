import pytest

from billing.models import Card
from orders.models import Order


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_complete_order(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/order/create/', {
            **kwargs,
        },
        format='multipart', expected_status_code=kwargs.get("expected_status_code", 200),
    )


def test_complete_order_api_with_saving_card(
    mocker,
    stripe_response,
    call_complete_order, 
    complete_order_request, 
    cart,
    billing_profile,
):
    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)
    response = call_complete_order(**complete_order_request)

    order_id = response["order_id"]
    order = Order.objects.get(order_id=order_id)
    billing_profile = order.billing_profile

    card = Card.objects.filter(billing_profile=billing_profile).first()
    assert card.default == True

    payment_method = order.payment_method
    assert payment_method.stripe_token == complete_order_request["card_token"]
    assert payment_method.type == "CARD"
    assert payment_method.card == card


def test_complete_order_without_saving_card(
    call_complete_order,
    complete_order_request,
    cart,
    billing_profile,
):
    complete_order_request["remember_card"] = False
    response = call_complete_order(**complete_order_request)

    order_id = response["order_id"]
    order = Order.objects.get(order_id=order_id)
    billing_profile = order.billing_profile

    assert not Card.objects.filter(billing_profile=billing_profile).exists()

    payment_method = order.payment_method
    assert payment_method.stripe_token == complete_order_request["card_token"]
    assert payment_method.type == "CARD"
    assert not payment_method.card


def test_complete_order_with_saved_card(
    mocker,
    call_complete_order,
    complete_order_request,
    cart,
    billing_profile,
    card,
):
    complete_order_request.pop("card_token")
    complete_order_request["payment_method"] = card.last4

    card_creator = mocker.patch("billing.services.CardCreator")

    response = call_complete_order(**complete_order_request)

    order_id = response["order_id"]
    order = Order.objects.get(order_id=order_id)
    billing_profile = order.billing_profile

    card_creator.assert_not_called()

    payment_method = order.payment_method
    assert payment_method.stripe_token == card.stripe_id
    assert payment_method.type == "CARD"
    assert payment_method.card == card


def test_billing_profile_country_saving(
    mocker,
    mixer,
    call_complete_order,
    complete_order_request,
    cart,
    billing_profile,
    card
):
    order = mixer.blend("orders.Order", billing_profile=billing_profile, cart=cart)
    mocker.patch("orders.services.OrderToolkit.place_an_order", return_value=order)

    billing_profile.country = "BY"
    billing_profile.save()

    response = call_complete_order(**complete_order_request)

    billing_profile.refresh_from_db()
    assert billing_profile.country == "US"
import pytest

from orders.services import OrderToolkit


pytestmark = [pytest.mark.django_db]


def test_placing_an_order(billing_profile, cart_with_course, stripe_token):
    order = OrderToolkit.place_an_order(
        billing_profile=billing_profile,
        cart=cart_with_course,
        stripe_token=stripe_token,
    )

    assert order.order_id
    assert order.billing_profile == billing_profile
    assert order.cart == cart_with_course
    assert order.total == cart_with_course.total
    assert order.payment_method.type == "CARD"
    assert order.payment_method.stripe_token == stripe_token
    assert order.billing_profile.cards.count() == 0


def test_placing_an_order_with_card_saving(
    mocker,
    billing_profile, 
    cart_with_course, 
    stripe_token, 
    stripe_response,
):
    mocker.patch("app.integrations.stripe.AppStripe.create_card", return_value=stripe_response)

    order = OrderToolkit.place_an_order(
        billing_profile=billing_profile,
        cart=cart_with_course,
        stripe_token=stripe_token,
        save_card=True,
    )

    assert order.order_id
    assert order.billing_profile == billing_profile
    assert order.cart == cart_with_course
    assert order.total == cart_with_course.total
    assert order.payment_method.type == "CARD"
    assert order.payment_method.stripe_token == stripe_token

    card = billing_profile.cards.first()
    assert card.default == True


def test_placing_an_order_with_saved_card(
    billing_profile,
    cart_with_course,
    card,
):
    order = OrderToolkit.place_an_order(
        billing_profile=billing_profile,
        cart=cart_with_course,
        card_last4=card.last4,
    )

    assert order.order_id
    assert order.billing_profile == billing_profile
    assert order.cart == cart_with_course
    assert order.total == cart_with_course.total
    assert order.payment_method.type == "CARD"
    assert order.payment_method.stripe_token == card.stripe_id
    assert order.payment_method.card == card

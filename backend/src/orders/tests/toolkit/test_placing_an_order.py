import pytest

from orders.services import OrderToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def stripe_response():
    return {
        "id": "card_1JD9PPAGKJR9v1iNUvmLh76d",
        "brand": "Visa",
        "country": "US",
        "cvc_check": "pass",
        "exp_month": 4,
        "exp_year": 2024,
        "last4": "4242",
        "address_zip": "242424",
    }


@pytest.fixture
def stripe_token():
    return "tok_1JD9PPAGKJR9v1iNRcWACVHa"


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

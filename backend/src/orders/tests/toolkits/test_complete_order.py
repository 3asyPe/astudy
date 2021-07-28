import pytest

from app.errors import ValidationError
from orders.services import OrderToolkit


pytestmark = [pytest.mark.django_db]


def test_complete_order(mocker, billing_profile, cart_with_course, stripe_token):
    order = mocker.patch("orders.models.Order")
    charge = mocker.patch("orders.models.Charge")
    place_an_order = mocker.patch("orders.services.OrderToolkit.place_an_order", return_value=order)
    charge_for_order = mocker.patch("orders.services.OrderToolkit.charge_for_order", return_value=charge)
    ship_order = mocker.patch("orders.services.OrderToolkit.ship_order", return_value=order)
    close_order = mocker.patch("orders.services.OrderToolkit.close_order", return_value=order)

    OrderToolkit.complete_order(
        billing_profile=billing_profile,
        cart=cart_with_course,
        stripe_token=stripe_token,
    )

    place_an_order.assert_called_once()
    charge_for_order.assert_called_once()
    ship_order.assert_called_once()
    close_order.assert_called_once()


def test_not_commiting_changes_until_its_all_done(
    mocker, 
    billing_profile, 
    cart_with_course,
    stripe_token,
    charge_stripe_response,
):
    mocker.patch("app.integrations.stripe.AppStripe.create_charge", return_value=charge_stripe_response)
    
    cart_with_course.total = 0
    cart_with_course.save()

    with pytest.raises(ValidationError):
        OrderToolkit.complete_order(
            billing_profile=billing_profile,
            cart=cart_with_course,
            stripe_token=stripe_token,
        )

    cart_with_course.total = cart_with_course.courses.first().price
    cart_with_course.save()

    order = OrderToolkit.complete_order(
        billing_profile=billing_profile,
        cart=cart_with_course,
        stripe_token=stripe_token,
    )

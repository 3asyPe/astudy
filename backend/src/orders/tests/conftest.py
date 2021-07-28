import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order(mixer, billing_profile, cart_with_course, payment_method):
    return mixer.blend(
        "orders.Order",
        billing_profile=billing_profile,
        cart=cart_with_course,
        payment_method=payment_method,
        total=cart_with_course.total,
    )


@pytest.fixture
def charge(mixer, order, stripe_charge_id):
    return mixer.blend(
        "orders.Charge",
        order=order,
        billing_profile=order.billing_profile,
        payment_method=order.payment_method,
        stripe_id=stripe_charge_id,
        amount=order.total,
    )


@pytest.fixture
def payment_method(mixer, stripe_token):
    return mixer.blend(
        "orders.PaymentMethod",
        type="CARD",
        stripe_token=stripe_token,
    )


@pytest.fixture
def cart_with_course(cart, course_factory):
    cart.courses.add(course_factory())
    return cart


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
def charge_stripe_response():
    return {
        "id": "ch_1JGoWa2eZvKYlo2CbxvMiOyL",
        "paid": True,
    }


@pytest.fixture
def stripe_token():
    return "tok_1JD9PPAGKJR9v1iNRcWACVHa"    


@pytest.fixture
def stripe_charge_id():
    return "ch_1JGoWa2eZvKYlo2CbxvMiOyL"

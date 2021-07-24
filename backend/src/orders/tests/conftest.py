import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order(mixer, billing_profile, cart, payment_method):
    return mixer.blend(
        "orders.Order",
        billing_profile=billing_profile,
        cart=cart,
        payment_method=payment_method,
    )


@pytest.fixture
def payment_method(mixer):
    return mixer.blend(
        "orders.PaymentMethod",
        type="CARD",
        stripe_token="tok_test",
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
def stripe_token():
    return "tok_1JD9PPAGKJR9v1iNRcWACVHa"    

import pytest


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

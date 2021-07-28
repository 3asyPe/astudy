import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def charge_stripe_error_response():
    return {
        "id": "ch_1JGoWa2eZvKYlo2CbxvMiOyL",
        "paid": False,
        "failure_message": "Test failure message",
    }

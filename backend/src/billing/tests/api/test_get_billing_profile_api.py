import pytest

from billing.models import BillingProfile
from billing.services import BillingProfileToolkit


pytestmark = [pytest.mark.django_db]


def test_get_billing_profile_api_with_user(api, billing_profile):
    response = api.get("/api/billing/get/")

    assert response["country"] == "Canada"
    assert response["postal_code"] == "666666"
    
    card = response["cards"][0]
    assert card["brand"] == "VISA"
    assert card["last4"] == "4242"
    assert card["default"] == False


def test_get_billing_profile_api_with_anonymous_user(anon, billing_profile):
    response = anon.get("/api/billing/get/", expected_status_code=401)


def test_get_nonexistent_billing_profile_api(api, mocker):
    user = api.user
    qs = BillingProfile.objects.filter(user=user)
    if qs.exists():
        qs.first().delete()

    response = api.get("/api/billing/get/")

    assert response["country"]
    assert "postal_code" in response
    assert "cards" in response

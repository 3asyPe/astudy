import pytest

from billing.models import BillingProfile
from billing.services import BillingProfileToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(user):
    billing_profile = BillingProfile.objects.get(user=user)
    billing_profile.delete()
    return user


def test_get_billing_profile(billing_profile, mocker):
    create_new_billing_profile = mocker.patch(
        "billing.services.BillingProfileToolkit.create_new_billing_profile"
    )
    user = billing_profile.user
    obj = BillingProfileToolkit.get_or_create_billing_profile(user)
    
    assert obj == billing_profile
    create_new_billing_profile.assert_not_called()


def test_create_billing_profile(user, mocker):
    create_new_billing_profile = mocker.patch(
        "billing.services.BillingProfileToolkit.create_new_billing_profile"
    )
    BillingProfileToolkit.get_or_create_billing_profile(user)

    create_new_billing_profile.assert_called_once()

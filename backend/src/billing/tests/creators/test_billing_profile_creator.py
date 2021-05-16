import pytest

from accounts.utils import AccountErrorMessages
from app.errors import ValidationError
from billing.services import BillingProfileCreator
from billing.utils import BillingProfileErrorMessages


pytestmark = [pytest.mark.django_db]


def test_create_billing_profile_with_default_info(user):
    billing_profile = BillingProfileCreator(
        user=user,
    )()

    assert billing_profile.user == user
    assert billing_profile.country == "United States of America"
    assert billing_profile.postal_code == None
    assert billing_profile.active == True


def test_create_billing_profile_with_custom_data(user):
    billing_profile = BillingProfileCreator(
        user=user,
        country="Belarus",
        postal_code=213023,
        customer_id="randomstring",
    )()

    assert billing_profile.user == user
    assert billing_profile.country == "Belarus"
    assert billing_profile.postal_code == 213023
    assert billing_profile.customer_id == "randomstring"
    assert billing_profile.active == True


def test_create_already_existing_billing_profile(user, billing_profile):
    with pytest.raises(ValidationError) as exc:
        new_billing_profile = BillingProfileCreator(
            user=user
        )()
    
    assert str(exc.value) == BillingProfileErrorMessages.BILLING_PROFILE_ALREADY_EXISTS_ERROR.value


def test_create_billing_profile_with_anonymous_user(anonymous_user):
    with pytest.raises(ValidationError) as exc:
        billing_profile = BillingProfileCreator(
            user=anonymous_user,
        )()

    assert str(exc.value) == AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value

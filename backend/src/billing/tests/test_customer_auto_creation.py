import pytest

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(user):
    BillingProfile.objects.filter(user=user).delete()
    return user


def test_customer_creation_after_billing_profile_creation(mixer, mocker, settings, user):
    settings.STRIPE_API_TURNED_ON = True
    create_customer = mocker.patch("app.integrations.stripe.AppStripe.create_customer", return_value={"id": 123})
    
    billing_profile = mixer.blend("billing.BillingProfile", user=user)

    create_customer.assert_called_once()
    assert billing_profile.customer_id == 123


def test_customer_creation_if_billing_does_not_have_customer_id(mocker, settings, billing_profile):
    settings.STRIPE_API_TURNED_ON = True
    create_customer = mocker.patch("app.integrations.stripe.AppStripe.create_customer", return_value={"id": 123})

    billing_profile.customer_id = None
    billing_profile.save()

    create_customer.assert_called_once()
    assert billing_profile.customer_id == 123


def test_no_customer_auto_creation_if_stripe_api_is_turned_off(mocker, billing_profile):
    create_customer = mocker.patch("app.integrations.stripe.AppStripe.create_customer", return_value={"id": 123})

    billing_profile.customer_id = None
    billing_profile.save()

    create_customer.assert_not_called()
    assert billing_profile.customer_id == None
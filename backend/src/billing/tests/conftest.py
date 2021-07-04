import pytest

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def billing_profile(mixer, user):
    qs = BillingProfile.objects.filter(user=user, active=True)
    if qs.exists():
        return qs.first()
    return mixer.blend("billing.BillingProfile", user=user)

@pytest.fixture
def card(mixer, billing_profile):
    card = mixer.blend(
        "billing.Card",
        billing_profile=billing_profile, 
        brand="VISA", 
        country="Belarus",
        last4="4242",
    )
    return card
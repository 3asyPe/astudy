import pytest

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def billing_profile(api, mixer):
    qs = BillingProfile.objects.filter(user=api.user, active=True)
    if qs.exists():
        billing_profile = qs.first()
    else:
        billing_profile = mixer.blend(
            "billing.BillingProfile", 
            user=api.user,
        )

    billing_profile.country = "Canada"
    billing_profile.save()

    card = mixer.blend(
        "billing.Card",
        billing_profile=billing_profile, 
        brand="VISA", 
        country="Belarus",
        last4="4242",
        postal_code="424242",
    )
    billing_profile.cards.add(card)
    return billing_profile
    
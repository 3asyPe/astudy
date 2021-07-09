import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def card(mixer, billing_profile):
    card = mixer.blend(
        "billing.Card",
        billing_profile=billing_profile, 
        brand="VISA", 
        country="Belarus",
        postal_code="424242",
        last4="4242",
    )
    return card
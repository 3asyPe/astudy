import pytest

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def complete_order_request(stripe_token):
    return {
        "card_token": stripe_token,
        "country": "US",
        "payment_method": "newPaymentCard",
        "remember_card": "true",
    }


@pytest.fixture
def cart(api, cart, course_factory):
    cart.user = api.user
    cart.courses.add(course_factory())
    return cart


@pytest.fixture
def billing_profile(api, mixer):
    qs = billing_profile = BillingProfile.objects.filter(user=api.user)
    if qs.exists():
        return qs.first()
    return mixer.blend("billing.BillingProfile", user=api.user)


@pytest.fixture
def card(card, billing_profile):
    card.billing_profile = billing_profile
    card.save()
    return card

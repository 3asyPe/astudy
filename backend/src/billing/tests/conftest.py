import pytest

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def billing_profile(mixer, user):
    qs = BillingProfile.objects.filter(user=user, active=True)
    if qs.exists():
        return qs.first()
    return mixer.blend("billing.BillingProfile", user=user)
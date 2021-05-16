import pytest

from django.contrib.auth import get_user_model

from billing.models import BillingProfile


pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create(
        email="newuseremail@gmail.com",
        password="newpassword",
    )


def test_billing_profile_auto_creation(user):
    assert BillingProfile.objects.get(user=user)
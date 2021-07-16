import random
import string

import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient
from billing.models import BillingProfile
from carts.models import Wishlist


User = settings.AUTH_USER_MODEL

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def api():
    return DRFClient()


@pytest.fixture
def anon():
    return DRFClient(anon=True)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    return mixer.blend(User, email="testemail@gmail.com")


@pytest.fixture
def another_user(mixer):
    return mixer.blend(User, email="testemail2@gmail.com")


@pytest.fixture
def anonymous_user(mixer):
    return AnonymousUser()


@pytest.fixture
def course_factory(mixer):
    def course_mixer():
        return mixer.blend(
            "courses.Course", 
            title=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
            subtitle=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
            price=3.33,
            description=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
        )
    return course_mixer


@pytest.fixture
def cart(mixer, user):
    return mixer.blend("carts.Cart", user=user)


@pytest.fixture
def wishlist(user):
    return Wishlist.objects.get_or_create(user=user)[0]


@pytest.fixture
def saved_for_later(mixer, user):
    return mixer.blend("carts.SavedForLater", user=user)


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
        stripe_id="card_1JD9PPAGKJR9v1iNUvmLh76d",
        brand="VISA", 
        country="Belarus",
        postal_code="424242",
        last4="4242",
    )
    return card

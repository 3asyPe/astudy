import random
import string

import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient


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

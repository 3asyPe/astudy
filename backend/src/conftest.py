import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient


User = settings.AUTH_USER_MODEL


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
def anonymous_user(mixer):
    return AnonymousUser()

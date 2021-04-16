import pytest

from rest_framework.authtoken.models import Token

from accounts.services import UserCreator


pytestmark = [pytest.mark.django_db]


def test_token_after_creating_user():
    created = UserCreator(data={
        "email": "someemail@gmail.com",
        "password": "testpassword",
    })()

    assert Token.objects.get(user=created)

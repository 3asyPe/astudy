import logging
import pytest
import random
import string

from rest_framework.authtoken.models import Token

from accounts.utils import AccountErrorMessages


logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.django_db]


def test_auth_with_existing_user(anon, user, user_token):
    response = anon.post("/api/auth/", {
        "email": "test@gmail.com",
        "password": "testpassword",
    }, expected_status_code=200)

    assert response["token"] == user_token.key
    assert response["user_id"] == user.id
    assert response["email"] == user.email


def test_auth_with_new_user(anon, mixer):
    email = "randomemail@gmail.com"
    password = ''.join([random.choice(string.hexdigits) for _ in range(0, 8)])
    user = mixer.blend("accounts.User", email=email)
    user.set_password(password)
    user.save()
    token = Token.objects.create(user=user)

    response = anon.post("/api/auth/", {
        "email": email,
        "password": password,
    }, expected_status_code=200)

    assert response["token"] == token.key
    assert response["user_id"] == user.id
    assert response["email"] == user.email


@pytest.mark.parametrize("email, password", [
    ["non-existent-email@gmail.com", "randompassword"],
    ["test@gmail.com", "asdf"],
    ["email@gmail.com", "testpassword"],
])
def test_auth_with_wrong_credentials(anon, user, email, password):
    response = anon.post("/api/auth/", {
        "email": email,
        "password": password,
    }, expected_status_code=400)

    assert response["error"] == AccountErrorMessages.CREDENTIALS_ERROR.value


def test_auth_with_inactive_user(anon, user):
    user.is_active = False
    user.save()
    
    response = anon.post("/api/auth/", {
        "email": "test@gmail.com",
        "password": "testpassword",
    }, expected_status_code=400)

    assert response["error"] == AccountErrorMessages.DISABLED_ACCOUNT_ERROR.value


@pytest.mark.parametrize("email, password",[
    [None, None],
    ["test@gmail.com", None],
    [None, "testpassword"]
])
def test_auth_without_required_fields(anon, user, email, password):
    response = anon.post("/api/auth/", {
        "email": email,
        "password": password,
    }, expected_status_code=400)


def test_auth_with_additional_request_fields(anon, user, user_token):
    response = anon.post("/api/auth/", {
        "email": "test@gmail.com",
        "password": "testpassword",
        "field1": "randomtext",
        "field2": 123123,
    }, expected_status_code=200)

    assert response["token"] == user_token.key
    assert response["user_id"] == user.id
    assert response["email"] == user.email
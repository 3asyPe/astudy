import pytest
import logging

from rest_framework.authtoken.models import Token

from accounts.models import User


logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("email, password", [
    ["test_email@gmail.com", "testpassword"]
])
def test_created_account(api, email, password):
    response = api.post("/api/registration/", {
        "email": email,
        "password": password
    })

    user = User.objects.get(email=email)

    assert user.is_admin == False


@pytest.mark.parametrize("email, password", [
    ["test_email@gmail.com", "testpassword"]
])
def test_compare_created_account_with_response(api, email, password):
    response = api.post("/api/registration/", {
        "email": email,
        "password": password
    })

    user = User.objects.get(email=email)
    token = Token.objects.get(user=user)

    assert response["token"] == token.key
    assert response["user_id"] == user.id
    assert response["email"] == user.email
    assert response["admin"] == user.is_admin


@pytest.mark.parametrize("email, password", [
    ["somestring", "testpassword"],
    ["", "testpassword"],
    ["test_email@gmail.com", "wrong"],
    ["test_email@gmail.com", ""],
    ["", ""],
])
def test_creation_with_invalid_credentials(api, email, password):
    response = api.post("/api/registration/", {
        "email": email,
        "password": password,
    }, expected_status_code=400)


def test_creation_without_email(api):
    response = api.post("/api/registration/", {
        "password": "testpassword",
    }, expected_status_code=400)


def test_creation_without_password(api):
    response = api.post("/api/registration/", {
        "email": "testemail@gmail.com",
    }, expected_status_code=400)


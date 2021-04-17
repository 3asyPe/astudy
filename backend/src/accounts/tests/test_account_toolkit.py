import pytest

from accounts.services import AccountToolkit


pytestmark = [pytest.mark.django_db]


def test_authentication(user, user_token):
    auth_user, token = AccountToolkit.authenticate(data={
        "email":"test@gmail.com", 
        "password":"testpassword",
    })
    assert auth_user == user
    assert token == user_token
    assert auth_user.is_authenticated

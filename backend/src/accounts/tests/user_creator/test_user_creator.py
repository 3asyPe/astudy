import pytest

from rest_framework.exceptions import ValidationError as RestValidationError

from accounts.services import UserCreator
from accounts.utils import AccountErrorMessages
from app.errors import ValidationError


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("email, password", [
    ("e@gmail.com", "testpass"),
    ("somelongtestemailwithloadsofchars@gmail.com", "somelongtestpassword123")
])
def test_user_creator_with_valide_data(email, password):
    created = UserCreator(data={
        "email": email,
        "password": password,
    })()

    created.refresh_from_db()

    assert created.email == email
    assert created.is_active == True


@pytest.mark.parametrize("email, password", [
    ("validemail@gmail.com", "invpass"),
    ("validemail@gmail.com", 123),
])
def test_user_creator_with_invalid_password(email, password):
    with pytest.raises(ValidationError) as exc:
        created = UserCreator(data={
            "email": email,
            "password": password,
        })()

    assert str(exc.value) == AccountErrorMessages.INCORRECT_PASSWORD_SCHEME_ERROR.value


@pytest.mark.parametrize("email", ['somestring', '', None])
def test_user_creator_with_invalid_email(email):
    with pytest.raises(RestValidationError) as exc:
        created = UserCreator(data={
            "email": email,
            "password": "somepassword"
        })()


@pytest.mark.parametrize("password", ['', None])
def test_user_creator_with_empty_password(password):
    with pytest.raises(RestValidationError) as exc:
        created = UserCreator(data={
            "email": "someemail@gmail.com",
            "password": password,
        })()

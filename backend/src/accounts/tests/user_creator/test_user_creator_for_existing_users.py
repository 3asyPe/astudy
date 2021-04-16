import pytest

from accounts.services import UserCreator
from accounts.utils import AccountErrorMessages
from app.errors import ValidationError


pytestmark = [pytest.mark.django_db]


def test_creating_existing_user(user):
    with pytest.raises(ValidationError) as exc:
        created = UserCreator(data={
            "email": "test@gmail.com",
            "password": "testpassword",
        })()

    assert str(exc.value) == AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value


def test_user_with_same_email(user):
    with pytest.raises(ValidationError) as exc:
        created = UserCreator(data={
            "email": "test@gmail.com",
            "password": "newpassword",
        })()

    assert str(exc.value) == AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value


def test_user_with_same_email_case_is_case_insensetive(user):
    with pytest.raises(ValidationError) as exc:
        created = UserCreator(data={
            "email": "TeST@GmaIl.COm",
            "password": "somepassword",
        })()

    assert str(exc.value) == AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value

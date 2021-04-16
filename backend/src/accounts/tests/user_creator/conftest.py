import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(mixer):
    return mixer.blend("accounts.User", email="test@gmail.com", password="testpassword")
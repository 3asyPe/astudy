import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(mixer, user):
    return mixer.blend("carts.Cart", user=user)


@pytest.fixture
def cart_without_user(mixer):
    return mixer.blend("carts.Cart", user=None)

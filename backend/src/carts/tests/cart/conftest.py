import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(mixer, user):
    return mixer.blend("carts.Cart", user=user)


@pytest.fixture
def another_cart(mixer, another_user):
    return mixer.blend("carts.Cart", user=another_user)


@pytest.fixture
def cart_without_user(mixer):
    return mixer.blend("carts.Cart", user=None)


@pytest.fixture
def inactive_cart(mixer, user):
    return mixer.blend("carts.Cart", user=user, active=False)

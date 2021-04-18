import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, api):
    cart.user = api.user
    cart.save()
    return cart

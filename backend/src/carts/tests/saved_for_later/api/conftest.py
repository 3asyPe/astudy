import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, api):
    cart.user = api.user
    cart.save()
    return cart


@pytest.fixture
def saved_for_later(saved_for_later, api):
    saved_for_later.user = api.user
    saved_for_later.save()
    return saved_for_later
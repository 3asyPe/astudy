import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart_without_user(mixer):
    return mixer.blend("carts.Cart", user=None)

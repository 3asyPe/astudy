import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, api):
    cart.user = api.user
    cart.save()
    return cart


@pytest.fixture
def wishlist(cart):
    user = cart.user
    wishlist = Wishlist.objects.get_or_create(user=user)
    return wishlist[0]

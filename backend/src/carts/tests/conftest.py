import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(mixer, user):
    return mixer.blend("carts.Cart", user=user)


@pytest.fixture
def cart_without_user(mixer):
    return mixer.blend("carts.Cart", user=None)


@pytest.fixture
def wishlist(mixer, user):
    return Wishlist.objects.get_or_create(user=user)[0]


@pytest.fixture
def saved_for_later(mixer, user):
    return mixer.blend("carts.SavedForLater", user=user)

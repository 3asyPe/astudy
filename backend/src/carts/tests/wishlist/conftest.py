import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def wishlist(mixer, user):
    return mixer.blend("carts.Wishlist", user=user)
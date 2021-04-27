import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def wishlist(mixer, user):
    return Wishlist.objects.get_or_create(user=user)[0]
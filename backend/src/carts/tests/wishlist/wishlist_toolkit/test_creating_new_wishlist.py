import pytest

from carts.models import Wishlist
from carts.services import WishlistToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(user):
    Wishlist.objects.filter(user=user).delete()
    return user


def test_create_new_wishlist(mocker, user, another_user):
    wishlist = Wishlist.objects.get_or_create(user=another_user)
    create_wishlist = mocker.patch(
        "carts.services.WishlistToolkit._create_wishlist",
        return_value=wishlist
    )

    WishlistToolkit.create_new_wishlist(user=user)

    create_wishlist.assert_called_once()



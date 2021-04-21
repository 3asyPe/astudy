import pytest

from accounts.utils import AccountErrorMessages
from carts.models import Wishlist
from carts.services import WishlistToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(user):
    Wishlist.objects.filter(user=user).delete()
    return user


def test_load_existing_wishlist(wishlist):
    got = WishlistToolkit.load_wishlist(user=wishlist.user)

    assert got == wishlist


def test_load_non_existing_wishlist(user):
    wishlist = WishlistToolkit.load_wishlist(user=user)

    assert wishlist.user == user
    assert wishlist.courses.count() == 0


def test_load_non_existing_wishlist_call_create_method(mocker, user):
    wishlist = Wishlist.objects.create(user=user)
    create_wishlist = mocker.patch(
        "carts.services.WishlistToolkit._create_wishlist",
        return_value = wishlist
    )
    got = WishlistToolkit.load_wishlist(user=user)

    assert create_wishlist.called_once()


def test_load_wishlist_with_anonymoun_user(anonymous_user):
    with pytest.raises(PermissionError) as exc:
        wishlist = WishlistToolkit.load_wishlist(user=anonymous_user)

    assert str(exc.value) == AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value


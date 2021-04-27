import pytest

from accounts.utils import AccountErrorMessages
from app.errors import ValidationError
from carts.models import Wishlist
from carts.services import WishlistToolkit
from carts.utils import WishlistErrorMessages


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

    got = WishlistToolkit.create_new_wishlist(user=user)

    create_wishlist.assert_called_once()


def test_create_new_wishlist_with_anonymous_user(anonymous_user):
    with pytest.raises(PermissionError) as exc:
        got = WishlistToolkit.create_new_wishlist(user=anonymous_user)
    
    assert str(exc.value) == AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value


def test_create_already_existed_wishlist(user):
    wishlist = Wishlist.objects.create(user=user)
    with pytest.raises(ValidationError) as exc:
        got = WishlistToolkit.create_new_wishlist(user=user)
    
    assert str(exc.value) == WishlistErrorMessages.WISHLIST_ALREADY_EXISTS_ERROR.value

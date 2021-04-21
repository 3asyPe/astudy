import pytest

from accounts.utils import AccountErrorMessages
from app.errors import ValidationError
from carts.models import Wishlist
from carts.services import WishlistCreator
from carts.utils import WishlistErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(user):
    Wishlist.objects.filter(user=user).delete()
    return user


def test_create_wishlist(user):
    wishlist = WishlistCreator(user=user)()
    
    assert wishlist.user == user
    assert wishlist.courses.count() == 0


def test_create_wishlist_with_anonymous_user(anonymous_user):
    with pytest.raises(PermissionError) as exc:
        wishlist = WishlistCreator(user=anonymous_user)()

    assert str(exc.value) == AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value


def test_create_wishlist_for_user_with_existings_wishlist(user):
    wish = Wishlist.objects.create(user=user)
    with pytest.raises(ValidationError) as exc:
        wishlist = WishlistCreator(user=user)()
    
    assert str(exc.value) == WishlistErrorMessages.WISHLIST_ALREADY_EXISTS_ERROR.value

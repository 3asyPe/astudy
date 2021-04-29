import pytest 

from django.contrib.auth import get_user_model

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]

User = get_user_model()


def user():
    return User.objects.create(
        email="newuseremail@gmail.com",
        password="newpassword"
    )


def test_wishlist_creation_for_new_user(user):
    assert Wishlist.objects.get(user=user)
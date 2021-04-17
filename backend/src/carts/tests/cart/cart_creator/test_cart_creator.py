import pytest

from app.errors import ValidationError
from carts.models import Cart
from carts.services import CartCreator
from carts.utils import CartErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


def test_cart_creation_with_user(user):
    cart = CartCreator(user=user)()

    assert cart.user == user
    assert cart.courses.count() == 0
    assert cart.total == 0
    assert cart.subtotal == 0
    assert cart.active == True


def test_cart_creation_without_user():
    cart = CartCreator()()

    assert cart.user == None
    assert cart.courses.count() == 0
    assert cart.total == 0
    assert cart.subtotal == 0
    assert cart.active == True


def test_cart_with_anonymous_user(anonymous_user):
    cart = CartCreator(user=anonymous_user)()

    assert cart.user == None
    assert cart.courses.count() == 0
    assert cart.total == 0
    assert cart.subtotal == 0
    assert cart.active == True


def test_cart_creation_for_user_with_existing_cart(cart, user):
    with pytest.raises(ValidationError) as exc:
        new_cart = CartCreator(user=user)()
    
    assert str(exc.value) == CartErrorMessages.CART_ALREADY_EXISTS_ERROR.value

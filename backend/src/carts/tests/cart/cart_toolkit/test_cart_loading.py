import pytest

from carts.services import CartToolkit, CartCreator


pytestmark = [pytest.mark.django_db]


def test_cart_loading_with_user_and_id_for_same_cart(cart):
    test_cart = CartToolkit.load_cart(user=cart.user, cart_id=cart.id)

    assert test_cart == cart


def test_cart_loading_with_user(cart):
    test_cart = CartToolkit.load_cart(user=cart.user)

    assert test_cart == cart


def test_cart_loading_with_id(cart):
    test_cart = CartToolkit.load_cart(cart_id=cart.id)
    
    assert test_cart == cart


def test_cart_loading_with_user_and_different_cart_id(cart, another_cart):
    test_cart = CartToolkit.load_cart(user=cart.user, cart_id=another_cart.id)

    assert test_cart == cart


def test_cart_loading_for_user_without_existing_cart(class_mocker, user):
    cart_creator = class_mocker.patch("carts.services.CartCreator")
    test_cart = CartToolkit.load_cart(user=user)

    assert cart_creator.called_once()
    

def test_cart_loading_without_arguments(class_mocker):
    cart_creator = class_mocker.patch("carts.services.CartCreator")
    test_cart = CartToolkit.load_cart()

    assert cart_creator.called_once()


def test_cart_loading_updating_totals(mocker, cart):
    cart_update_totals = mocker.patch("carts.models.Cart.update_totals")
    test_cart = CartToolkit.load_cart(user=cart.user)

    assert cart_update_totals.called_once()


def test_loading_inactive_cart(class_mocker, inactive_cart):
    cart_creator = class_mocker.patch("carts.services.CartCreator")
    test_cart = CartToolkit.load_cart(user=inactive_cart.user, cart_id=inactive_cart.id)

    assert cart_creator.called_once()
    assert test_cart != inactive_cart


def test_loading_active_and_inactive_cart_with_same_user_with_proper_user(cart, inactive_cart):
    test_cart = CartToolkit.load_cart(user=cart.user, cart_id=inactive_cart.id)
    
    assert test_cart == cart


def test_loading_active_and_inactive_cart_with_same_user_with_proper_id(cart, inactive_cart):
    test_cart = CartToolkit.load_cart(user=inactive_cart.user, cart_id=cart.id)

    assert test_cart == cart

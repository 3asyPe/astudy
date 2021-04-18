import pytest


pytestmark = [pytest.mark.django_db]


def test_get_cart_info_api(api, cart):
    response = api.get("/api/cart/info/", {
        "cart_id": cart.id,
    })

    assert response["id"] == cart.id
    assert float(response["subtotal"]) == cart.subtotal
    assert float(response["total"]) == cart.total


def test_get_cart_info_without_user(anon, cart_without_user):
    response = anon.get('/api/cart/info/', {
        "cart_id": cart_without_user.id
    })

    assert response["id"] == cart_without_user.id


def test_get_cart_info_without_id(api, cart):
    response = api.get("/api/cart/info/", {})

    assert response["id"] == cart.id


def test_get_cart_info_without_anything(anon):
    response = anon.get("/api/cart/get/", {})

    assert "id" in response
    assert "subtotal" in response
    assert "total" in response
import pytest


pytestmark = [pytest.mark.django_db]


def test_get_courses_count_api(api, cart):
    response = api.get("/api/cart/count/", {
        "cart_id": cart.id,
    })

    assert response["cart_id"] == cart.id
    assert response["cart_courses_count"] == cart.courses.count()


def test_get_courses_count_api_call_method(mocker, api, cart):
    get_courses_count = mocker.patch(
        "carts.models.Cart.get_courses_count", 
        return_value=cart.courses.count()
    )
    response = api.get("/api/cart/count/", {
        "cart_id": cart.id,
    })

    get_courses_count.assert_called_once()


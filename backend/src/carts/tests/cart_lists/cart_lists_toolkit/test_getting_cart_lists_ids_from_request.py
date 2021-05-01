import pytest

from unittest.mock import Mock

from carts.services import CartListsToolkit


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("request_data", [
    {
        "GET": {
            "cart_id": 1,
            "saved_for_later_id": 1,
        }
    },
    {
        "GET": {
            "cart_id": 2,
        }
    },
    {
        "GET": {
            "saved_for_later_id": 2,
        }
    },
    {
        "GET": {}
    }
])
def test_getting_cart_ids_from_get_request(request_data, request):
    request.GET = request_data["GET"]
    request.POST = {}
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)

    assert ids["cart_id"] == request.GET.get("cart_id")
    assert ids["saved_for_later_id"] == request.GET.get("saved_for_later_id")


@pytest.mark.parametrize("request_data", [
    {
        "POST": {
            "cart_id": 1,
            "saved_for_later_id": 1,
        }
    },
    {
        "POST": {
            "cart_id": 2,
        }
    },
    {
        "POST": {
            "saved_for_later_id": 2,
        }
    }, 
    {
        "POST": {}
    }
])
def test_getting_cart_ids_from_post_request(request_data, request):
    request.POST = request_data["POST"]
    request.GET = {}
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)

    assert ids["cart_id"] == request.POST.get("cart_id")
    assert ids["saved_for_later_id"] == request.POST.get("saved_for_later_id")
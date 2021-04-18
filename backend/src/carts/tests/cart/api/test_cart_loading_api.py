import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart_with_course(cart, course_factory):
    cart.courses.add(course_factory())
    return cart


@pytest.fixture
def cart_with_applied_coupon(mixer, cart):
    coupon = mixer.blend("discounts.Coupon", code="testcode")
    applied_coupon = mixer.blend("discounts.AppliedCoupon", coupon=coupon, cart=cart)
    return cart


@pytest.fixture
def mocked_cart_lists_method(mocker, cart):
    mocker.patch(
        "carts.services.CartListsSelector.get_cart_lists_by_user_and_ids",
        return_value={"cart": cart}
    )


def test_loading_cart_api(api, cart):
    response = api.get("/api/cart/get/", {
        "cart_id": cart.id,
    })

    assert response["id"] == cart.id
    assert "courses" in response
    assert "applied_coupons" in response
    assert float(response["subtotal"]) == cart.subtotal
    assert float(response["total"]) == cart.total


def test_loading_cart_without_user(anon, cart_without_user):
    response = anon.get('/api/cart/get/', {
        "cart_id": cart_without_user.id
    })

    assert response["id"] == cart_without_user.id


def test_loading_cart_without_id(api, cart):
    response = api.get("/api/cart/get/", {})

    assert response["id"] == cart.id


def test_loading_cart_without_anything(anon):
    response = anon.get("/api/cart/get/", {})

    assert "id" in response
    assert "courses" in response
    assert "applied_coupons" in response
    assert "subtotal" in response
    assert "total" in response


def test_loading_cart_courses(api, cart_with_course):
    response = api.get("/api/cart/get/", {
        "cart_id": cart_with_course.id
    })

    course = cart_with_course.courses.first()
    res_course = response["courses"][0]

    assert res_course["slug"] == course.slug
    assert str(course.image) in res_course["image"]
    assert res_course["title"] == course.title
    assert res_course["subtitle"] == course.subtitle
    assert res_course["price"] == str(course.price)
    assert "discount" in res_course


def test_loading_cart_applied_coupons(api, cart_with_applied_coupon):
    response = api.get("/api/cart/get/", {
        "cart_id": cart_with_applied_coupon.id
    })

    applied_coupon = cart_with_applied_coupon.applied_coupons.first()
    res_applied_coupon = response["applied_coupons"][0]

    assert res_applied_coupon["code"] == applied_coupon.code

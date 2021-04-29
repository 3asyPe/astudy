import pytest
import logging

from carts.models import Wishlist


logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def wishlist_with_course(wishlist, course_factory):
    wishlist.courses.add(course_factory())
    return wishlist


@pytest.fixture
def api_user_without_wishlist(api):
    Wishlist.objects.filter(user=api.user).delete()


@pytest.fixture
def cart_with_applied_coupon(mixer, cart, wishlist_with_course):
    coupon = mixer.blend("discounts.Coupon", code="testcode", discount=10)
    course = wishlist_with_course.courses.first()
    coupon.applicable_to.add(course)
    applied_coupon = mixer.blend("discounts.AppliedCoupon", coupon=coupon, cart=cart)
    return cart


def test_loading_wishlist_api(api, wishlist):
    response = api.get("/api/wishlist/get/", {})

    assert "courses" in response


def test_loading_wishlist_courses(api, wishlist_with_course):
    response = api.get("/api/wishlist/get/", {})

    course = wishlist_with_course.courses.first()
    res_course = response["courses"][0] 

    assert res_course["slug"] == course.slug
    assert str(course.image) in res_course["image"]
    assert res_course["title"] == course.title
    assert res_course["subtitle"] == course.subtitle
    assert res_course["price"] == str(course.price)
    assert "discount" in res_course


def test_loading_wishlist_course_with_discount(api, wishlist_with_course, cart_with_applied_coupon):
    response = api.get("/api/wishlist/get/", {
        "cart_id": cart_with_applied_coupon.id,
    })

    course = wishlist_with_course.courses.first()
    res_course = response["courses"][0]
    discount = res_course["discount"]
    assert discount["course_slug"] == course.slug
    assert "new_price" in discount
    assert "applied_coupon" in discount


def test_loading_wishlist_with_anonymous_user(anon, cart_without_user):
    response = anon.get('/api/wishlist/get/', {
        "cart_id": cart_without_user.id
    }, expected_status_code=401)


def test_loading_not_created_wishlist(api, api_user_without_wishlist):
    response = api.get("/api/wishlist/get/", {})

    assert Wishlist.objects.filter(user=api.user).exists()
    assert "courses" in response

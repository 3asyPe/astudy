import pytest

from carts.models import Wishlist
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_add_to_wishlist(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/wishlist/add/', {
            **kwargs,
        },
        format='multipart', expected_status_code=kwargs.get("expected_status_code", 200),
    )


@pytest.fixture
def api_user_without_wishlist(api):
    Wishlist.objects.filter(user=api.user).delete()


def test_adding_course_to_wishlist_api(wishlist, cart, course_factory, call_add_to_wishlist, api):
    course = course_factory()
    response = call_add_to_wishlist(cart_id=cart.id, course_slug=course.slug)

    assert response['id'] == cart.id
    assert float(response['subtotal']) == float(response["total"]) == 0
    assert wishlist.courses.count() == 1
    assert wishlist.courses.first() == course


def test_adding_course_to_wishlist_with_anonymous_user(anon, cart, course_factory):
    course = course_factory()
    response = anon.post("/api/wishlist/add/", {
        "cart_id": cart.id,
        "course_slug": course.slug
    }, expected_status_code=401)


def test_adding_course_to_non_existed_wishlist(api, cart, call_add_to_wishlist, api_user_without_wishlist, course_factory):
    course = course_factory()
    response = api.post("/api/wishlist/add/", {
        "course_slug": course.slug
    }, format="multipart", expected_status_code=200)

    wishlist = Wishlist.objects.get(user=api.user)
    assert wishlist.courses.count() == 1
    assert wishlist.courses.first() == course
    

def test_adding_course_to_wishlist_api_call_add_method(mocker, cart, wishlist, course_factory, call_add_to_wishlist):
    add_to_wishlist = mocker.patch("carts.services.WishlistToolkit.add_course_to_wishlist", return_value=wishlist)
    
    course = course_factory()
    response = call_add_to_wishlist(cart_id=cart.id, course_slug=course.slug)

    add_to_wishlist.assert_called_once()

    
def test_adding_course_to_wishlist_api_call_delete_duplicates_method(mocker, cart, wishlist, course_factory, call_add_to_wishlist):
    delete_duplicates = mocker.patch("carts.services.CartListsToolkit.delete_duplicates_excluding_instance")

    course = course_factory()
    response = call_add_to_wishlist(cart_id=cart.id, course_slug=course.slug)

    delete_duplicates.assert_called_once()


def test_adding_course_to_wishlist_api_with_wrong_slug(cart, call_add_to_wishlist):
    response = call_add_to_wishlist(
        cart_id=cart.id, 
        course_slug="somerandomslug", 
        expected_status_code=400,
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value


def test_adding_course_to_wishlist_api_wihtout_slug(cart, call_add_to_wishlist):
    response = call_add_to_wishlist(
        cart_id=cart.id,
        expected_status_code=400,
    )

    assert response["error"] == CourseErrorMessages.REQUEST_FIELDS_ERROR.value
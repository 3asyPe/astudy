import pytest

from carts.utils import CartErrorMessages
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_remove_from_wishlist(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/wishlist/remove/', {
            **kwargs,
        },
        format='multipart',
        expected_status_code=kwargs.pop("expected_status_code", 200),
        empty_content=kwargs.pop("empty_content", True),
    )


@pytest.fixture
def wishlist_with_two_courses(wishlist, course_factory):
    wishlist.courses.add(course_factory())
    wishlist.courses.add(course_factory())
    return wishlist


def test_removing_course_from_wishlist_api(cart, wishlist_with_two_courses, call_remove_from_wishlist):
    wishlist = wishlist_with_two_courses
    course = wishlist.courses.last()
    response = call_remove_from_wishlist(
        cart_id=cart.id,
        course_slug=course.slug,
    )

    assert response == {}
    assert wishlist.courses.count() == 1
    assert wishlist.courses.first() != course


def test_removing_from_wishlist_not_added_course_api(cart, wishlist_with_two_courses, course_factory, call_remove_from_wishlist):
    wishlist = wishlist_with_two_courses
    course = course_factory()
    response = call_remove_from_wishlist(
        cart_id=cart.id,
        course_slug=course.slug,
    )

    assert response == {}
    assert wishlist.courses.count() == 2


def test_removing_course_from_wishlist_api_with_wrong_slug(cart, wishlist_with_two_courses, call_remove_from_wishlist):
    wishlist = wishlist_with_two_courses
    response = call_remove_from_wishlist(
        cart_id=cart.id,
        course_slug="somerandomslug",
        expected_status_code=400,
        empty_content=False,
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value
    assert wishlist.courses.count() == 2


def test_removing_course_from_wishlist_api_wihtout_slug(cart, wishlist_with_two_courses, call_remove_from_wishlist):
    wishlist = wishlist_with_two_courses
    response = call_remove_from_wishlist(
        cart_id=cart.id,
        expected_status_code=400,
        empty_content=False
    )

    assert response["error"] == CartErrorMessages.REQUEST_FIELDS_ERROR.value
    assert wishlist.courses.count() == 2


def test_removing_course_from_wishlist_api_call_remove_method(
    mocker, 
    cart, 
    wishlist_with_two_courses, 
    call_remove_from_wishlist,
):
    wishlist = wishlist_with_two_courses
    remove_course = mocker.patch("carts.services.WishlistToolkit.remove_course_from_wishlist", return_value=wishlist)
    course = wishlist.courses.last()
    response = call_remove_from_wishlist(
        cart_id=cart.id,
        course_slug=course.slug,
    )    

    remove_course.assert_called_once()

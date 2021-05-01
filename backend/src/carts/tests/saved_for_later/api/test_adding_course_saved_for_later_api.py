import pytest

from carts.utils import CartErrorMessages
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_add_to_s_list(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/savedforlater/add/', {
            **kwargs,
        },
        format='multipart', 
        expected_status_code=kwargs.pop("expected_status_code", 200),
    )


def test_adding_course_to_s_list_api(cart, saved_for_later, course_factory, call_add_to_s_list):
    course = course_factory()
    response = call_add_to_s_list(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        course_slug=course.slug
    )

    assert response['id'] == cart.id
    assert float(response['subtotal']) == float(response["total"]) == 0
    assert saved_for_later.courses.count() == 1
    assert saved_for_later.courses.first() == course


def test_adding_course_to_s_list_api_call_add_method(
    mocker, 
    cart,
    saved_for_later, 
    course_factory,
    call_add_to_s_list,
):
    add_course = mocker.patch(
        "carts.services.SavedForLaterToolkit.add_course_to_saved_for_later",
        return_value=saved_for_later
    )
    course = course_factory()
    response = call_add_to_s_list(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        course_slug=course.slug
    )

    add_course.assert_called_once()


def test_adding_course_to_s_list_api_call_delete_duplicates_method(
    mocker, 
    cart, 
    saved_for_later,
    course_factory, 
    call_add_to_s_list
):
    delete_duplicates = mocker.patch("carts.services.CartListsToolkit.delete_duplicates_excluding_instance")

    course = course_factory()
    response = call_add_to_s_list(
        cart_id=cart.id, 
        saved_for_later_id=saved_for_later.id,
        course_slug=course.slug
    )

    delete_duplicates.assert_called_once()


def test_adding_course_to_s_list_api_with_wrong_slug(cart, saved_for_later, call_add_to_s_list):
    response = call_add_to_s_list(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        course_slug="somerandomslug",
        expected_status_code=400
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value


def test_adding_course_to_s_list_api_without_slug(cart, saved_for_later, call_add_to_s_list):
    response = call_add_to_s_list(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        expected_status_code=400
    )

    assert response["error"] == CartErrorMessages.REQUEST_FIELDS_ERROR.value
import pytest

from carts.utils import CartErrorMessages
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_remove_from_s_list(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/savedforlater/remove/', {
            **kwargs,
        },
        format='multipart',
        expected_status_code=kwargs.pop("expected_status_code", 200),
        empty_content=kwargs.pop("empty_content", True),
    )


@pytest.fixture
def s_list_with_two_courses(saved_for_later, course_factory):
    saved_for_later.courses.add(course_factory())
    saved_for_later.courses.add(course_factory())
    return saved_for_later


def test_remove_course_from_s_list_api(cart, s_list_with_two_courses, call_remove_from_s_list):
    s_list = s_list_with_two_courses
    course = s_list.courses.last()
    response = call_remove_from_s_list(
        cart_id=cart.id,
        saved_for_later_id=s_list.id,
        course_slug=course.slug,    
    )

    assert response == {}
    assert s_list.courses.count() == 1
    assert s_list.courses.first() != course


def test_remove_course_from_s_list_not_added_course_api(
    cart, 
    s_list_with_two_courses, 
    course_factory, 
    call_remove_from_s_list
):
    s_list = s_list_with_two_courses
    course = course_factory()
    response = call_remove_from_s_list(
        cart_id=cart.id,
        saved_for_later_id=s_list.id,
        course_slug=course.slug
    )

    assert response == {}
    assert s_list.courses.count() == 2


def test_remove_course_from_s_list_api_with_wrong_slug(cart, s_list_with_two_courses, call_remove_from_s_list):
    s_list = s_list_with_two_courses
    response = call_remove_from_s_list(
        cart_id=cart.id,
        saved_for_later_id=s_list.id,
        course_slug="somerandomslug",
        expected_status_code=400,
        empty_content=False
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value
    assert s_list.courses.count() == 2


def test_remove_course_from_s_list_api_without_slug(cart, s_list_with_two_courses, call_remove_from_s_list):
    s_list = s_list_with_two_courses
    response = call_remove_from_s_list(
        cart_id=cart.id,
        saved_for_later_id=s_list.id,
        expected_status_code=400,
        empty_content=False
    )

    assert response["error"] == CartErrorMessages.REQUEST_FIELDS_ERROR.value
    assert s_list.courses.count() == 2


def test_remove_course_from_s_list_api_call_remove_method(
    mocker, 
    cart, 
    s_list_with_two_courses, 
    call_remove_from_s_list,
):
    s_list = s_list_with_two_courses
    remove_course = mocker.patch(
        "carts.services.SavedForLaterToolkit.remove_course_from_saved_for_later", 
        return_value=s_list
    )
    course = s_list.courses.last()
    response = call_remove_from_s_list(
        cart_id=cart.id,
        saved_for_later_id=s_list.id,
        course_slug=course.slug,
    )    

    remove_course.assert_called_once()

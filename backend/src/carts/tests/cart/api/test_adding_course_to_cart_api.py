import pytest 

from carts.utils import CartErrorMessages
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_add_to_cart(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/cart/add/', {
            **kwargs,
        },
        format='multipart', expected_status_code=kwargs.get("expected_status_code", 200),
    )


def test_adding_course_to_cart_api(cart, course_factory, call_add_to_cart, api):
    course = course_factory()
    response = call_add_to_cart(cart_id=cart.id, course_slug=course.slug)

    assert response['id'] == cart.id
    assert float(response['subtotal']) == float(response["total"]) == float(course.price)
    assert cart.courses.count() == 1
    assert cart.courses.first() == course


def test_adding_course_to_cart_api_call_add_method(mocker, cart, course_factory, call_add_to_cart):
    add_to_cart = mocker.patch("carts.services.CartToolkit.add_course_to_cart", return_value=cart)
    
    course = course_factory()
    response = call_add_to_cart(cart_id=cart.id, course_slug=course.slug)

    add_to_cart.assert_called_once()

    
def test_adding_course_to_cart_api_call_delete_duplicates_method(mocker, cart, course_factory, call_add_to_cart):
    delete_duplicates = mocker.patch("carts.services.CartListsToolkit.delete_duplicates_excluding_instance")

    course = course_factory()
    response = call_add_to_cart(cart_id=cart.id, course_slug=course.slug)

    delete_duplicates.assert_called_once()


def test_adding_course_to_cart_api_with_wrong_slug(cart, call_add_to_cart):
    response = call_add_to_cart(
        cart_id=cart.id, 
        course_slug="somerandomslug", 
        expected_status_code=400,
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value


def test_adding_course_to_cart_api_wihtout_slug(cart, call_add_to_cart):
    response = call_add_to_cart(
        cart_id=cart.id,
        expected_status_code=400,
    )

    assert response["error"] == CourseErrorMessages.REQUEST_FIELDS_ERROR.value

import pytest

from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def call_remove_from_cart(api, **kwargs):
    return lambda **kwargs: api.post(
        '/api/cart/remove/', {
            **kwargs,
        },
        format='multipart', expected_status_code=kwargs.get("expected_status_code", 200),
    )


@pytest.fixture
def cart_with_two_courses(cart, course_factory):
    cart.courses.add(course_factory())
    cart.courses.add(course_factory())
    return cart


def test_removing_course_from_cart_api(cart_with_two_courses, call_remove_from_cart):
    cart = cart_with_two_courses
    course = cart.courses.last()
    response = call_remove_from_cart(
        cart_id=cart.id,
        course_slug=course.slug,
    )

    assert response['id'] == cart.id
    assert float(response['subtotal']) == float(response["total"]) == float(course.price)
    assert cart.courses.count() == 1


def test_removing_from_cart_api_not_added_course(cart_with_two_courses, course_factory, call_remove_from_cart):
    cart = cart_with_two_courses
    course = course_factory()
    response = call_remove_from_cart(
        cart_id=cart.id,
        course_slug=course.slug
    )

    total = cart.courses.first().price + cart.courses.last().price
    assert response["id"] == cart.id
    assert float(response['subtotal']) == float(response["total"]) == float(total)
    assert cart.courses.count() == 2


def test_removing_course_from_cart_api_with_wrong_slug(cart, call_remove_from_cart):
    response = call_remove_from_cart(
        cart_id=cart.id,
        course_slug="somerandomslug",
        expected_status_code=400
    )

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value


def test_removing_course_from_cart_api_wihtout_slug(cart, call_remove_from_cart):
    response = call_remove_from_cart(
        cart_id=cart.id,
        expected_status_code=400
    )

    assert response["error"] == CourseErrorMessages.REQUEST_FIELDS_ERROR.value


def test_removing_course_from_cart_api_call_remove_method(mocker, cart_with_two_courses, call_remove_from_cart):
    cart = cart_with_two_courses
    remove_course = mocker.patch("carts.services.CartToolkit.remove_course_from_cart", return_value=cart)
    course = cart.courses.last()
    response = call_remove_from_cart(
        cart_id=cart.id,
        course_slug=course.slug,
    )    

    remove_course.assert_called_once()

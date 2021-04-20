import pytest

from carts.utils import CartErrorMessages
from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


def test_check_on_course_already_in_cart_api_with_course(api, cart, course_factory):
    course = course_factory()
    cart.courses.add(course)
    response = api.get("/api/cart/checkalreadyin/", {
        "cart_id": cart.id,
        "course_slug": course.slug,
    })

    assert response["course_already_in_cart"] == True


def test_check_on_course_already_in_cart_api_without_course(api, cart, course_factory):
    course = course_factory()
    response = api.get("/api/cart/checkalreadyin/", {
        "cart_id": cart.id,
        "course_slug": course.slug,
    })

    assert response["course_already_in_cart"] == False


def test_check_on_course_already_in_cart_api_with_wrong_slug(api, cart):
    response = api.get("/api/cart/checkalreadyin/", {
        "cart_id": cart.id,
        "course_slug": "somerandomslug",
    }, expected_status_code=400)

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value


def test_check_on_course_already_in_cart_without_slug(api, cart):
    response = api.get("/api/cart/checkalreadyin/", {
        "cart_id": cart.id,
    }, expected_status_code=400)

    assert response["error"] == CartErrorMessages.REQUEST_FIELDS_ERROR.value

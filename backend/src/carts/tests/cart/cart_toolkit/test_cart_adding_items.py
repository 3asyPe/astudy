import pytest

from carts.services import CartToolkit
from courses.models import Course


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def unpublished_course(course_factory):
    course = course_factory()
    course.published = False
    course.save()

    course.refresh_from_db()
    return course


@pytest.mark.parametrize("courses_count", [0, 3, 15])
def test_add_courses_to_cart(courses_count, cart, course_factory):
    for i in range(courses_count):
        CartToolkit.add_course_to_cart(cart=cart, course_slug=course_factory().slug)
    
    cart.refresh_from_db()

    assert cart.courses.count() == courses_count


def test_add_course_to_cart(course_factory, cart):
    assert cart.courses.count() == 0
    course = course_factory()

    CartToolkit.add_course_to_cart(cart=cart, course_slug=course.slug)

    cart.refresh_from_db()
    test_course = cart.courses.first()

    assert test_course == course


def test_add_course_with_wrong_slug(cart):
    with pytest.raises(Course.DoesNotExist):
        CartToolkit.add_course_to_cart(cart=cart, course_slug="somerandomslug")

    assert cart.courses.count() == 0


def test_add_unpublished_course(cart, unpublished_course):
    with pytest.raises(Course.DoesNotExist):
        CartToolkit.add_course_to_cart(cart=cart, course_slug=unpublished_course.slug)

    assert cart.courses.count() == 0

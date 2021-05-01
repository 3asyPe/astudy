import pytest

from carts.services import CartToolkit
from courses.models import Course


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart_with_one_course(course, cart):
    cart.courses.add(course)
    return cart


@pytest.fixture
def course(mixer):
    return mixer.blend("courses.Course", slug="test-slug")


@pytest.mark.parametrize("course_count", [0, 3, 5])
def test_remove_courses_from_cart(course_factory, cart, course_count):
    courses = []
    for i in range(course_count):
        course = course_factory()
        cart.courses.add(course)
        courses.append(course)

    for i in range(course_count):
        CartToolkit.remove_course_from_cart(cart=cart, course_slug=courses[-1].slug)

        assert courses[-1] not in cart.courses.all()
        assert cart.courses.count() == course_count - i - 1

        courses.pop(-1)
    

def test_remove_not_added_course_from_cart(course_factory, cart):
    CartToolkit.remove_course_from_cart(cart=cart, course_slug=course_factory().slug)
    
    assert cart.courses.count() == 0


def test_remove_course_with_wrong_slug_from_cart(cart):
    with pytest.raises(Course.DoesNotExist):
        CartToolkit.remove_course_from_cart(cart=cart, course_slug="somerandomslug")

    assert cart.courses.count() == 0


def test_removing_course_from_cart_updating_totals(mocker, cart_with_one_course, course):
    update_totals = mocker.patch("carts.models.Cart.update_totals")
    CartToolkit.remove_course_from_cart(cart=cart_with_one_course, course_slug=course.slug)

    update_totals.assert_called_once()


import pytest

from carts.services import WishlistToolkit
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
def test_remove_courses_from_cart(course_factory, wishlist, course_count):
    courses = []
    for i in range(course_count):
        course = course_factory()
        wishlist.courses.add(course)
        courses.append(course)

    for i in range(course_count):
        WishlistToolkit.remove_course_from_wishlist(wishlist=wishlist, course_slug=courses[-1].slug)

        assert courses[-1] not in wishlist.courses.all()
        assert wishlist.courses.count() == course_count - i - 1

        courses.pop(-1)

    
def test_remove_not_added_course(course_factory, wishlist):
    WishlistToolkit.remove_course_from_wishlist(wishlist=wishlist, course_slug=course_factory().slug)
    
    assert wishlist.courses.count() == 0


def test_remove_course_with_wrong_slug(wishlist):
    with pytest.raises(Course.DoesNotExist):
        WishlistToolkit.remove_course_from_wishlist(wishlist=wishlist, course_slug="somerandomslug")

    assert wishlist.courses.count() == 0
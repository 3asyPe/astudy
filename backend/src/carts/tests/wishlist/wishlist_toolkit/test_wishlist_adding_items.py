import pytest

from carts.services import WishlistToolkit
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
def test_add_courses_to_cart(courses_count, wishlist, course_factory):
    for i in range(courses_count):
        WishlistToolkit.add_course_to_wishlist(wishlist=wishlist, course_slug=course_factory().slug)
    
    wishlist.refresh_from_db()

    assert wishlist.courses.count() == courses_count


def test_add_course_to_wishlist(wishlist, course_factory):
    course = course_factory()
    WishlistToolkit.add_course_to_wishlist(wishlist=wishlist, course_slug=course.slug)

    wishlist.refresh_from_db()

    test_course = wishlist.courses.first()
    assert wishlist.courses.count() == 1
    assert test_course == course


def test_add_already_added_course_to_wishlist(wishlist, course_factory):
    course = course_factory()
    wishlist.courses.add(course)
    WishlistToolkit.add_course_to_wishlist(wishlist=wishlist, course_slug=course.slug)

    wishlist.refresh_from_db()

    assert wishlist.courses.count() == 1


def test_add_to_wishlist_course_with_wrong_slug(wishlist):
    with pytest.raises(Course.DoesNotExist) as exc:
        WishlistToolkit.add_course_to_wishlist(
            wishlist=wishlist,
            course_slug="somerandomslug"
        )

    wishlist.refresh_from_db()

    assert wishlist.courses.count() == 0


def test_add_unpublished_course_to_wishlist(wishlist, unpublished_course):
    with pytest.raises(Course.DoesNotExist) as exc:
        WishlistToolkit.add_course_to_wishlist(
            wishlist=wishlist,
            course_slug=unpublished_course.slug
        )

    wishlist.refresh_from_db()

    assert wishlist.courses.count() == 0

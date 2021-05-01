import pytest

from carts.services import CartListsToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart_lists_with_same_course(cart, wishlist, saved_for_later, course_factory):
    course = course_factory()
    cart.courses.add(course)
    wishlist.courses.add(course)
    saved_for_later.courses.add(course)
    return {
        "cart": cart,
        "wishlist": wishlist,
        "saved_for_later": saved_for_later,
    }


def test_deleting_duplicates_excluding_cart(cart_lists_with_same_course):
    cart = cart_lists_with_same_course["cart"]
    course = cart.courses.first()

    CartListsToolkit.delete_duplicates_excluding_instance(
        course_slug=course.slug,
        instance=cart,
        **cart_lists_with_same_course
    )

    assert cart.courses.count() == 1
    assert cart_lists_with_same_course["wishlist"].courses.count() == 0
    assert cart_lists_with_same_course["saved_for_later"].courses.count() == 0

    assert cart.courses.first() == course


def test_deleting_duplicates_excluding_wishlist(cart_lists_with_same_course):
    wishlist = cart_lists_with_same_course["wishlist"]
    course = wishlist.courses.first()

    CartListsToolkit.delete_duplicates_excluding_instance(
        course_slug=course.slug,
        instance=wishlist,
        **cart_lists_with_same_course
    )

    assert wishlist.courses.count() == 1
    assert cart_lists_with_same_course["cart"].courses.count() == 0
    assert cart_lists_with_same_course["saved_for_later"].courses.count() == 0

    assert wishlist.courses.first() == course


def test_deleting_duplicates_excluding_saved_for_later(cart_lists_with_same_course):
    saved_for_later = cart_lists_with_same_course["saved_for_later"]
    course = saved_for_later.courses.first()

    CartListsToolkit.delete_duplicates_excluding_instance(
        course_slug=course.slug,
        instance=saved_for_later,
        **cart_lists_with_same_course
    )

    assert saved_for_later.courses.count() == 1
    assert cart_lists_with_same_course["cart"].courses.count() == 0
    assert cart_lists_with_same_course["wishlist"].courses.count() == 0

    assert saved_for_later.courses.first() == course
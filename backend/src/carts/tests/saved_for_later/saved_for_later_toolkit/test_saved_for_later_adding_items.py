import pytest

from carts.services import SavedForLaterToolkit
from courses.models import Course


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize("courses_count", [0, 3, 15])
def test_add_courses_to_cart(courses_count, saved_for_later, course_factory):
    for i in range(courses_count):
        SavedForLaterToolkit.add_course_to_saved_for_later(
            s_list=saved_for_later, 
            course_slug=course_factory().slug
        )
    
    saved_for_later.refresh_from_db()

    assert saved_for_later.courses.count() == courses_count


def test_add_course_to_s_list(saved_for_later, course_factory):
    course = course_factory()
    SavedForLaterToolkit.add_course_to_saved_for_later(
        s_list=saved_for_later,
        course_slug=course.slug,
    )

    saved_for_later.refresh_from_db()
    assert saved_for_later.courses.count() == 1
    assert saved_for_later.courses.first() == course


def test_add_course_with_wrong_slug_to_s_list(saved_for_later, course_factory):
    with pytest.raises(Course.DoesNotExist):
        SavedForLaterToolkit.add_course_to_saved_for_later(
            s_list=saved_for_later,
            course_slug="somerandomslug"
        )

    saved_for_later.refresh_from_db()
    assert saved_for_later.courses.count() == 0


def test_add_unpublished_course_to_s_list(saved_for_later, course_factory):
    with pytest.raises(Course.DoesNotExist):
        SavedForLaterToolkit.add_course_to_saved_for_later(
            s_list=saved_for_later,
            course_slug="somerandomslug",
        )

    saved_for_later.refresh_from_db()
    assert saved_for_later.courses.count() == 0
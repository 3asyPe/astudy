import pytest

from carts.services import SavedForLaterToolkit
from courses.models import Course


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def s_list_with_one_course(course, saved_for_later):
    saved_for_later.courses.add(course)
    return saved_for_later


@pytest.fixture
def course(mixer):
    return mixer.blend("courses.Course", slug="test-slug")


@pytest.mark.parametrize("course_count", [0, 3, 5])
def test_remove_course_from_s_list(course_factory, saved_for_later, course_count):
    courses = []
    for i in range(course_count):
        course = course_factory()
        saved_for_later.courses.add(course)
        courses.append(course)

    for i in range(course_count):
        SavedForLaterToolkit.remove_course_from_saved_for_later(
            s_list=saved_for_later, 
            course_slug=courses[-1].slug
        )

        assert courses[-1] not in saved_for_later.courses.all()
        assert saved_for_later.courses.count() == course_count - i - 1

        courses.pop(-1)


def test_remove_not_added_course_from_s_list(course_factory, saved_for_later):
    SavedForLaterToolkit.remove_course_from_saved_for_later(
        s_list=saved_for_later,
        course_slug=course_factory().slug
    )

    assert saved_for_later.courses.count() == 0 


def test_remove_course_with_wrong_slug_from_s_list(saved_for_later):
    with pytest.raises(Course.DoesNotExist):
        SavedForLaterToolkit.remove_course_from_saved_for_later(
            s_list=saved_for_later,
            course_slug="somerandomslug"
        )

    assert saved_for_later.courses.count() == 0

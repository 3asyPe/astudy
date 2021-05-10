import pytest

from courses.services import CourseToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def course(course):
    course.content.sections_count = 0
    course.content.save()
    return course


def test_recalculation_course_content_tree_by_section(course):
    section = course.content.sections.first()

    CourseToolkit.recalculate_course_content_tree_by_section(instance=section)

    assert course.content.sections_count == 2


def test_recalculation_course_content_tree_by_section_call_method(mocker, course):
    recalculate_sections = mocker.patch("courses.models.CourseContent.recalculate_sections")
    section = course.content.sections.first()

    CourseToolkit.recalculate_course_content_tree_by_section(instance=section)

    recalculate_sections.assert_called_once()
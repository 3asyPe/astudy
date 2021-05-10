import pytest

from courses.services import CourseToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def course(course):
    course.content.lectures_count = 0
    
    for section in course.content.sections.all():
        section.lectures_count = 0
        section.save()

    course.content.save()

    return course


def test_recalculate_course_content_tree_by_lecture(course):
    lecture1 = course.content.sections.first().lectures.first()
    lecture2 = course.content.sections.last().lectures.first()

    CourseToolkit.recalculate_course_content_tree_by_lecture(instance=lecture1)
    CourseToolkit.recalculate_course_content_tree_by_lecture(instance=lecture2)

    for section in course.content.sections.all():
        assert section.lectures_count == 2

    assert course.content.lectures_count == 4


def test_recalculate_course_content_tree_by_lecture_call_method(mocker, course):
    recalculate_section = mocker.patch("courses.models.CourseSection.recalculate_lectures")
    recalculate_content = mocker.patch("courses.models.CourseContent.recalculate_lectures")

    lecture = course.content.sections.first().lectures.first()

    CourseToolkit.recalculate_course_content_tree_by_lecture(instance=lecture)

    recalculate_section.assert_called_once()
    recalculate_content.assert_called_once()
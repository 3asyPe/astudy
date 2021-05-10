import pytest


pytestmark = [pytest.mark.django_db]


def test_recalculation_content_tree_after_creating_new_lecture(mocker, mixer, course):
    recalculate_content_tree = mocker.patch("courses.services.CourseToolkit.recalculate_course_content_tree_by_lecture")

    lecture = mixer.blend("courses.CourseLecture", course_section=course.content.sections.first())

    recalculate_content_tree.assert_called_once()


def test_recalculation_content_tree_after_deleting_lecture(mocker, course):
    recalculate_content_tree = mocker.patch("courses.services.CourseToolkit.recalculate_course_content_tree_by_lecture")

    lecture = course.content.sections.first().lectures.first()
    lecture.delete()

    recalculate_content_tree.assert_called_once()


def test_recalculation_content_tree_after_creating_section(mocker, mixer, course):
    recalculate_content_tree = mocker.patch("courses.services.CourseToolkit.recalculate_course_content_tree_by_section")

    section = mixer.blend("courses.CourseSection", course_content=course.content)

    recalculate_content_tree.assert_called_once()


def test_recalculation_content_tree_after_deleting_section(mocker, course):
    recalculate_content_tree = mocker.patch("courses.services.CourseToolkit.recalculate_course_content_tree_by_section")

    section = course.content.sections.first()
    section.delete()

    recalculate_content_tree.assert_called_once()

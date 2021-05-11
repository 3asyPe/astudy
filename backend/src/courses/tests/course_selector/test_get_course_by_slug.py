import pytest

from courses.models import Course
from courses.services import CourseSelector


pytestmark = [pytest.mark.django_db]


def test_get_course_by_slug(course):
    test_course = CourseSelector.get_course_by_slug(slug=course.slug)

    assert test_course == course


def test_get_course_by_wrong_slug(course):
    with pytest.raises(Course.DoesNotExist):
        CourseSelector.get_course_by_slug(slug="somerandomslug")


def test_get_unpublished_course(course):
    course.published = False
    course.save()

    with pytest.raises(Course.DoesNotExist):
        CourseSelector.get_course_by_slug(slug=course.save)
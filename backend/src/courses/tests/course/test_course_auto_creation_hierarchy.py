import pytest

from courses.models import (
    Course,
    CourseContent,
    CourseDurationTime,
    CourseLectureDurationTime,
    CourseSectionDurationTime,
)


pytestmark = [pytest.mark.django_db]


def test_auto_creation_after_course_creation(mixer):
    course = mixer.blend("courses.Course")

    assert CourseContent.objects.get(course=course)
    assert CourseDurationTime.objects.get(course_content=course.content)


def test_section_duration_time_creation(mixer, course):
    section = mixer.blend("courses.CourseSection", course_content=course.content)

    assert CourseSectionDurationTime.objects.get(course_section=section)
    

def test_lecture_duration_time_creation(mixer, course):
    section = course.content.sections.first()
    lecture = mixer.blend("courses.CourseLecture", course_section=section)

    assert CourseLectureDurationTime.objects.get(course_lecture=lecture)

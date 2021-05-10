import pytest

from courses.models import CourseLectureDurationTime


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def lecture(course):
    return course.content.sections.first().lectures.first()


@pytest.fixture
def lecture_without_d_time(lecture):
    lecture.duration_time.delete()
    return lecture


def test_recalculation_course_duration_time_tree_after_changing_lecture_duration_time(mocker, lecture):
    recalculate_duration_times = mocker.patch("courses.services.CourseToolkit.recalculate_course_duration_time_tree_by_lecture")

    lecture.duration_time.hours = lecture.duration_time.hours + 1
    lecture.duration_time.save()

    recalculate_duration_times.assert_called_once()


def test_recalculation_course_duration_time_tree_after_creating_lecture_duration_time(mocker, mixer, lecture_without_d_time):
    recalculate_duration_times = mocker.patch("courses.services.CourseToolkit.recalculate_course_duration_time_tree_by_lecture")

    duration_time = CourseLectureDurationTime.objects.create(course_lecture=lecture_without_d_time)

    recalculate_duration_times.assert_called_once()


def test_recalculation_course_duration_time_tree_after_deleting_lecture_duration_time(mocker, lecture):
    recalculate_duration_times = mocker.patch("courses.services.CourseToolkit.recalculate_course_duration_time_tree_by_lecture")

    lecture.duration_time.delete()

    recalculate_duration_times.assert_called_once()

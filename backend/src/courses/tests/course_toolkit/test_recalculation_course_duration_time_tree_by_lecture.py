import pytest

from courses.services import CourseToolkit


pytestmark = [pytest.mark.django_db]


def reset_main_duration_times(course):
    c_duration_time = course.content.duration_time
    c_duration_time.hours = 0
    c_duration_time.minutes = 0
    c_duration_time.save()

    for section in course.content.sections.all():
        section.duration_time.hours = 0
        section.duration_time.minutes = 0
        section.duration_time.save()


@pytest.mark.parametrize("duration_times", [
    {
        "hours": 7,
        "minutes": 35,
        "section1": {
            "hours": 4,
            "minutes": 20,
            "lecture1": {
                "hours": 2,
                "minutes": 30,
                "seconds": 9,
            },
            "lecture2": {
                "hours": 1,
                "minutes": 49,
                "seconds": 51,
            }
        },
        "section2": {
            "hours": 3,
            "minutes": 15,
            "lecture1": {
                "hours": 2,
                "minutes": 10,
                "seconds": 1,
            },
            "lecture2": {
                "hours": 1,
                "minutes": 5,
                "seconds": 30,
            }
        }
    }
])
def test_recalculating_course_duration_time_by_lecture(duration_times, course):
    c_duration_time = course.content.duration_time
    sections = course.content.sections.all()

    for section, i in zip(sections, range(1, sections.count() + 1)):
        for lecture, j in zip(section.lectures.all(), range(1, section.lectures.count() + 1)):
            lecture.duration_time.hours = duration_times[f"section{i}"][f"lecture{j}"]["hours"]
            lecture.duration_time.minutes = duration_times[f"section{i}"][f"lecture{j}"]["minutes"]
            lecture.duration_time.seconds = duration_times[f"section{i}"][f"lecture{j}"]["seconds"]
            lecture.duration_time.save()

    reset_main_duration_times(course)

    for section in sections:
        for lecture in section.lectures.all():
            CourseToolkit.recalculate_course_duration_time_tree_by_lecture(instance=lecture)

    c_duration_time.refresh_from_db()
    assert c_duration_time.hours == duration_times["hours"]
    assert c_duration_time.minutes == duration_times["minutes"]

    for section, i in zip(sections, range(1, sections.count())):
        section.duration_time.refresh_from_db()
        assert section.duration_time.hours == duration_times[f"section{i}"]["hours"]
        assert section.duration_time.minutes == duration_times[f"section{i}"]["minutes"]


def test_recalculating_course_duration_times_by_lecture_call_recalculations(mocker, course):
    recalculate_lecture = mocker.patch("courses.models.CourseLecture.recalculate_duration_time")
    recalculate_section = mocker.patch("courses.models.CourseSection.recalculate_duration_time")
    recalculate_content = mocker.patch("courses.models.CourseContent.recalculate_duration_time")

    lecture = course.content.sections.first().lectures.first()
    CourseToolkit.recalculate_course_duration_time_tree_by_lecture(instance=lecture)

    recalculate_lecture.assert_called_once()
    recalculate_section.assert_called_once()
    recalculate_content.assert_called_once()

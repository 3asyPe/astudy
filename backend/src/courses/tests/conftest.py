import random
import pytest

from courses.models import (
    CourseDurationTime,
    CourseLectureDurationTime,
    CourseSectionDurationTime,
)


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def course(mixer):
    obj = mixer.blend(
        "courses.Course",
        price=mixer.RANDOM,
        students_count=mixer.RANDOM,
    )

    section1 = mixer.blend("courses.CourseSection", course_content=obj.content)
    section2 = mixer.blend("courses.CourseSection", course_content=obj.content)

    lectures = mixer.cycle(4).blend(
        "courses.CourseLecture", 
        course_section=(section for section in [section1, section1, section2, section2]),
    )
    for l in lectures:
        l.duration_time.hours = 10
        l.duration_time.minutes = random.randint(0, 59)
        l.duration_time.seconds = random.randint(0, 59)
        l.duration_time.save()
    return obj

import logging

from django.db.models.query import QuerySet

from categories.models import Category
from courses.models import (
    Course,
    CourseContent,
    CourseDurationTime,
    CourseLectureDurationTime,
    CourseSectionDurationTime,
)

logger = logging.getLogger(__name__)


class CourseSelector:
    @classmethod
    def get_course_by_slug(cls, slug: str) -> Course:
        qs = Course.objects.filter(slug=slug)
        if qs.exists():
            if not qs.filter(published=True).exists():
                logger.warning(f"There was an attempt to get an unpublished course with slug - {slug}")
                raise Course.DoesNotExist()
            return qs.first()
        raise Course.DoesNotExist()
    
    @classmethod
    def get_courses_by_category(cls, category: Category) -> QuerySet[Course]:
        courses = Course.objects.filter(category=category, published=True)
        return courses

    @classmethod
    def get_course_content_by_course(cls, course: Course) -> CourseContent:
        qs = CourseContent.objects.filter(course=course)
        if not qs.exists():
            logger.error(f"Course - {course} doesn't have a content field")
            raise CourseContent.DoesNotExist()
        return qs.first()

    @classmethod
    def get_course_duration_time_by_course(cls, course: Course) -> CourseDurationTime:
        course_content = cls.get_course_content_by_course(course=course)
        if hasattr(course_content, "duration_time") and course_content.duration_time is not None:
            return course_content.duration_time
        else:
            logger.error(f"Course - {course} doesn't have a duration time field")
            raise CourseDurationTime.DoesNotExist()

    @classmethod
    def get_course_lectures_count_by_course(cls, course: Course) -> int:
        course_content = cls.get_course_content_by_course(course=course)
        return course_content.lectures_count

    @classmethod   
    def get_course_lecture_duration_times_by_section_duration_time(
            cls,
            sec_dur_time: CourseSectionDurationTime
        ) -> QuerySet[CourseLectureDurationTime]:
        course_section = sec_dur_time.course_section
        lectures = course_section.lectures.all()
        duration_times = CourseLectureDurationTime.objects.filter(course_lecture__in=lectures)
        return duration_times

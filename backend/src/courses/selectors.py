from categories.models import Category

from django.db.models.query import QuerySet

from .models import (
    Course,
    CourseContent,
    CourseDurationTime,
)


def get_course_by_slug(slug: str) -> Course:
    qs = Course.objects.filter(slug=slug)
    if not qs.exists():
        raise Course.DoesNotExist()
    return qs.first()


def get_courses_by_category(category: Category) -> QuerySet[Course]:
    courses = Course.objects.filter(category=category)
    return courses


def get_course_duration_time_by_course(course: Course) -> CourseDurationTime:
    qs = CourseContent.objects.filter(course=course)
    if not qs.exists():
        raise CourseContent.DoesNotExist()
    course_content = qs.first()
    if hasattr(course_content, "duration_time") and course_content.duration_time is not None:
        return course_content.duration_time
    else:
        raise CourseDurationTime.DoesNotExist()
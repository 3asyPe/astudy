from categories.models import Category
from django.db.models.query import QuerySet

from .models import Course


def get_course_by_slug(slug: str) -> Course:
    qs = Course.objects.filter(slug=slug)
    if not qs.exists():
        raise Course.DoesNotExist()
    return qs.first()


def get_courses_by_category(category: Category) -> QuerySet[Course]:
    courses = Course.objects.filter(category=category)
    return courses

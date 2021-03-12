import logging

from .models import (
    CourseLecture,
    CourseLectureDurationTime,
    CourseSection,
    CourseSectionDurationTime,
)


logger = logging.getLogger(__name__)


def recalculate_course_duration_time_tree_by_lecture(instance: CourseLecture):
    """Recounting in this order is important"""
    instance.recalculate_duration_time()

    course_section = instance.course_section
    if CourseSectionDurationTime.objects.filter(course_section=course_section):
        course_section.recalculate_duration_time()

    course_content = course_section.course_content
    course_content.recalculate_duration_time()

    logger.info("Course duration time tree was recalculated successfully")


def recalculate_course_content_tree_by_lecture(instance: CourseLecture):
    """Recounting in this order is important"""
    course_section = instance.course_section
    course_section.recalculate_lectures()

    course_content = course_section.course_content
    course_content.recalculate_lectures()

    logger.info("Course content tree was recalculated successfully")


def create_course_section_duration_time(course_section: CourseSection) -> CourseSectionDurationTime:
    return CourseSectionDurationTime.objects.get_or_create(course_section=course_section)


def create_course_lecture_duration_time(course_lecture: CourseLecture) -> CourseLectureDurationTime:
    return CourseLectureDurationTime.objects.get_or_create(course_lecture=course_lecture)

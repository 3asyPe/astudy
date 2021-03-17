import logging

from courses.models import (
    Course,
    CourseContent,
    CourseDurationTime,
    CourseLecture,
    CourseLectureDurationTime,
    CourseSection,
    CourseSectionDurationTime,
)


logger = logging.getLogger(__name__)


class CourseToolkit:
    @classmethod
    def recalculate_course_duration_time_tree_by_lecture(cls, instance: CourseLecture):
        """Recalculating in this order is important"""
        instance.recalculate_duration_time()

        course_section = instance.course_section
        if CourseSectionDurationTime.objects.filter(course_section=course_section).exists():
            course_section.recalculate_duration_time()

        course_content = course_section.course_content
        if CourseDurationTime.objects.filter(course_content=course_content).exists():
            course_content.recalculate_duration_time()

        logger.info("Course duration time tree was recalculated successfully")

    @classmethod
    def recalculate_course_content_tree_by_lecture(cls, instance: CourseLecture):
        """Recalculating in this order is important"""
        course_section = instance.course_section
        course_section.recalculate_lectures()

        course_content = course_section.course_content
        course_content.recalculate_lectures()

        logger.info("Course content tree was recalculated successfully")

    @classmethod
    def create_course_content(cls, course: Course) -> CourseContent:
        return CourseContent.objects.get_or_create(course=course)

    @classmethod
    def create_course_duration_time(cls, course_content: CourseContent) -> CourseDurationTime:
        return CourseDurationTime.objects.get_or_create(course_content=course_content)

    @classmethod
    def create_course_section_duration_time(cls, course_section: CourseSection) -> CourseSectionDurationTime:
        return CourseSectionDurationTime.objects.get_or_create(course_section=course_section)

    @classmethod
    def create_course_lecture_duration_time(cls, course_lecture: CourseLecture) -> CourseLectureDurationTime:
        return CourseLectureDurationTime.objects.get_or_create(course_lecture=course_lecture)
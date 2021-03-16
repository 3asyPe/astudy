import logging

from app.utils import generate_unique_slug

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from courses.models import (
    Course, 
    CourseContent, 
    CourseSection, 
    CourseLecture,
    CourseLectureDurationTime,
)
from courses.services import CourseToolkit


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Course)
def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)


@receiver(post_save, sender=Course)
def course_post_save_receiver(sender, instance: Course, created, *args, **kwargs):
    if created:
        CourseToolkit.create_course_content(course=instance)


@receiver(post_save, sender=CourseContent)
def course_content_post_save_receiver(sender, instance: CourseContent, created, *args, **kwargs):
    if created:
        CourseToolkit.create_course_duration_time(course_content=instance)


@receiver(post_save, sender=CourseSection)
def course_section_post_save_receiver(sender, instance: CourseSection, created, *args, **kwargs):
    if created:
        CourseToolkit.create_course_section_duration_time(course_section=instance)
        course_content = instance.course_content
        course_content.recalculate_sections()


@receiver(post_delete, sender=CourseSection)
def course_section_post_delete_receiver(sender, instance: CourseSection, *args, **kwargs):
    course_content = instance.course_content
    course_content.recalculate_sections()


@receiver(post_save, sender=CourseLecture)
def course_lecture_post_save_receiver(sender, instance: CourseLecture, created, *args, **kwargs):
    if created:
        CourseToolkit.create_course_lecture_duration_time(course_lecture=instance)
        CourseToolkit.recalculate_course_content_tree_by_lecture(instance)


@receiver(post_delete, sender=CourseLecture)
def course_lecture_post_delete_receiver(sender, instance: CourseLecture, *args, **kwargs):
    CourseToolkit.recalculate_course_content_tree_by_lecture(instance)


@receiver([post_save, post_delete], sender=CourseLectureDurationTime)
def course_lecture_duration_time_post_save_and_delete_receiver(sender, instance: CourseLectureDurationTime, *args, **kwargs):
    course_lecture = instance.course_lecture
    CourseToolkit.recalculate_course_duration_time_tree_by_lecture(course_lecture)

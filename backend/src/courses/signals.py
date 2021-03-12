import logging

from app.utils import generate_unique_slug

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import (
    Course, 
    CourseContent, 
    CourseSection, 
    CourseLecture,
)


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Course)
def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)


@receiver(post_save, sender=CourseSection)
def course_section_post_save_receiver(sender, instance: CourseSection, created, *args, **kwargs):
    if created:
        course_content = instance.course_content
        course_content.recount_sections()


@receiver(post_delete, sender=CourseSection)
def course_section_post_delete_receiver(sender, instance: CourseSection, *args, **kwargs):
    course_content = instance.course_content
    course_content.recount_sections()


@receiver(post_save, sender=CourseLecture)
def course_lecture_post_save_receiver(sender, instance: CourseLecture, created, *args, **kwargs):
    if created:
        course_section = instance.course_section
        course_section.recount_lectures()

        course_content = course_section.course_content
        course_content.recount_lectures()


@receiver(post_delete, sender=CourseLecture)
def course_lecture_post_delete_receiver(sender, instance: CourseLecture, *args, **kwargs):
    course_section = instance.course_section
    course_section.recount_lectures()

    course_content = course_section.course_content
    course_content.recount_lectures()

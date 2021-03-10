from app.utils import generate_unique_slug

from django.db.models.signals import pre_save, post_save

from .models import Course


def course_pre_save_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)


pre_save.connect(course_pre_save_slug_receiver, sender=Course)

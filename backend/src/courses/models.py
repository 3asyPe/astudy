import datetime

from app.utils import generate_unique_slug

from django.db import models
from django.db.models.signals import pre_save, post_save

from categories.models import Category

from .utils import get_course_upload_image_path


class Course(models.Model):
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name="courses", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to=get_course_upload_image_path)
    title = models.CharField(max_length=70)
    subtitle = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    description = models.TextField(max_length=5000)
    students_count = models.IntegerField(default=0)
    lections_count = models.IntegerField(default=0)
    duration_time = models.TimeField(default=datetime.time(0, 0, 0))

    def __str__(self):
        return self.title


def course_pre_save_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)

pre_save.connect(course_pre_save_slug_receiver, sender=Course)

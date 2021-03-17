from app.utils import generate_unique_slug

from django.db import models
from django.db.models.signals import pre_save, post_save


class Category(models.Model):
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    title = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.title


def product_pre_save_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)

pre_save.connect(product_pre_save_slug_receiver, sender=Category)

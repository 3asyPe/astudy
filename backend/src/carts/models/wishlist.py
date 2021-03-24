from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField("courses.Course", blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Wishlist")
        verbose_name_plural = ("Wishlists")

    def get_courses_count(self):
        return self.courses.all().count()

    def __str__(self):
        return f"{self.user.__str__()} | Wishlist"

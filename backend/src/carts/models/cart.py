import logging

from courses.models import Course

from django.conf import settings
from django.db import models


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Cart")
        verbose_name_plural = ("Carts")

    def get_courses_count(self):
        return self.courses.all().count()

    def update_totals(self):
        courses = self.courses.all()
        total = 0
        for course in courses:
            total += course.price
        if self.subtotal != total:
            self.subtotal = total
            self.save()

    def __str__(self):
        return f"{self.user.__str__()} | id - {self.id} | active - {self.active} | total - {self.total}"

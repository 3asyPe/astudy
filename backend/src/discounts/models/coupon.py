from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models


User = settings.AUTH_USER_MODEL


class Coupon(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    applicable_to = models.ManyToManyField("courses.Course", related_name="coupons")
    discount = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(100)])
    expires = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Coupon")
        verbose_name_plural = ("Coupons")
    
    @property
    def is_active(self):
        if self.expires:
            return self.timestamp < self.expires and self.active
        return self.active

    def __str__(self):
        return f"{self.code}"

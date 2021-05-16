from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=120, default="United States of America", blank=True, null=True)
    postal_code = models.CharField(max_length=120, blank=True, null=True)
    customer_id = models.CharField(max_length=120, blank=True, null=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Billing profile')
        verbose_name_plural = ("Billing profiles")

    def __str__(self):
        return f"{self.user.__str__()} | Billing profile"

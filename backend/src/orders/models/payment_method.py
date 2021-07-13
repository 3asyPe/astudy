from django.db import models
from django.conf import settings


class PaymentMethod(models.Model):
    type = models.CharField(max_length=50, choices=settings.PAYMENT_METHODS)
    stripe_token = models.CharField(max_length=120)
    
    card = models.ForeignKey("billing.Card", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = ("Payment Method")
        verbose_name_plural = ("Payment Methods")

    def __str__(self):
        return f"Payment Method | {self.type}"

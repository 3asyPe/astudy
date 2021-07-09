from django.db import models


class Card(models.Model):
    billing_profile = models.ForeignKey("billing.BillingProfile", on_delete=models.CASCADE, related_name="cards")
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=120, blank=True, null=True)
    exp_month = models.IntegerField(blank=True, null=True)
    exp_year = models.IntegerField(blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Card')
        verbose_name_plural = ('Cards')

    def __str__(self):
        return f"{self.billing_profile.__str__() | Card | {self.brand}}"

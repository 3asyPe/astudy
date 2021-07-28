from django.db import models


class Charge(models.Model):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE)
    billing_profile = models.ForeignKey("billing.BillingProfile", on_delete=models.CASCADE)
    payment_method = models.ForeignKey("orders.PaymentMethod", on_delete=models.SET_NULL, blank=True, null=True)

    stripe_id = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(default=1.00, max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Charge for order {self.order.order_id}"

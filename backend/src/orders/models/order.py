from django.db import models

from app.utils import generate_random_string


class Order(models.Model):
    order_id = models.CharField(max_length=120, unique=True, blank=True, primary_key=False)
   
    billing_profile = models.ForeignKey("billing.BillingProfile", on_delete=models.CASCADE)
    cart = models.OneToOneField("carts.Cart", on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    payment_method = models.OneToOneField("orders.PaymentMethod", on_delete=models.SET_NULL, blank=True, null=True)

    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Order')
        verbose_name_plural = ("Orders")

    @property
    def user(self):
        return self.billing_profile.user

    def set_new_order_id(self, order_id=None, save_instance=True):
        if order_id is not None and not Order.objects.filter(order_id=order_id).exists():
            self.order_id = order_id
            if save_instance:
                self.save()
        else:
            self.set_new_order_id(order_id=generate_random_string(), save_instance=save_instance)

    def set_paid(self, paid, save_instance=True):
        self.paid = paid
        if save_instance:
            self.save()

    def set_shipped(self, shipped, save_instance=True):
        self.shipped = shipped
        if save_instance:
            self.save()

    def __str__(self):
        return f"{self.user.__str__()} | Order {self.order_id}"

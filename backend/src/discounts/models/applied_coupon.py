from django.db import models


class AppliedCouponManager(models.Manager):
    def active_coupons(self):
        return self.get_queryset().filter(
            active=True, 
            coupon__active=True,
        )


class AppliedCoupon(models.Model):
    coupon = models.ForeignKey("discounts.Coupon", on_delete=models.CASCADE)
    cart = models.ForeignKey("carts.Cart", on_delete=models.CASCADE, related_name="applied_coupons")
    active = models.BooleanField(default=True)

    objects = AppliedCouponManager()

    class Meta:
        verbose_name = ("Applied coupon")
        verbose_name_plural = ("Applied coupons")

    @property
    def is_active(self):
        return self.coupon.is_active and self.active

    @property
    def discount(self):
        return self.coupon.discount

    @property
    def code(self):
        return self.coupon.code

    def __str__(self):
        return f"{self.cart.__str__()} - {self.coupon.__str__()}"

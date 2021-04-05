import logging

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from carts.services import CartToolkit
from discounts.models import AppliedCoupon, Coupon
from discounts.services import DiscountSelector


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Coupon)
def coupon_pre_save_receiver(sender, instance: Coupon, *args, **kwargs):
    qs = Coupon.objects.filter(pk=instance.pk)
    if qs.exists():
        old_instance = qs.first()
        instance.active = instance.is_active
        if not old_instance.active == instance.active:
            applied_coupons = AppliedCoupon.objects.filter(coupon=instance)
            for applied_coupon in applied_coupons:
                applied_coupon.active = instance.active
                applied_coupon.save()
            logger.debug(f"Applied coupons of coupon - {instance} were activated/deactived")


@receiver(post_save, sender=AppliedCoupon)
def applied_coupon_post_save_receiver(sender, instance: AppliedCoupon, *args, **kwargs):
    cart = instance.cart
    CartToolkit.update_cart_totals(cart=cart)


@receiver(post_delete, sender=AppliedCoupon)
def applied_coupon_post_delete_receiver(sender, instance: AppliedCoupon, *args, **kwargs):
    cart = instance.cart
    CartToolkit.update_cart_totals(cart=cart)

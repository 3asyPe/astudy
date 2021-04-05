from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from carts.models import Cart
from carts.services import CartToolkit


@receiver(m2m_changed, sender=Cart.courses.through)
def m2m_changed_cart_receiver(sender, instance: Cart, action, *args, **kwargs):
    if "post_" in action:
        CartToolkit.update_cart_totals(cart=instance)

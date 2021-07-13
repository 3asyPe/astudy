import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Order)
def pre_save_order_receiver(sender, instance: Order, *args, **kwargs):
    if not instance.order_id:
        instance.set_new_order_id(save_instance=False)

from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.models import BillingProfile
from billing.services import BillingProfileToolkit


@receiver(post_save, sender=BillingProfile)
def post_save_billing_profile_receiver(sender, instance: BillingProfile, *args, **kwargs):
    if instance.customer_id is None:
        BillingProfileToolkit.create_new_customer(billing_profile=instance)

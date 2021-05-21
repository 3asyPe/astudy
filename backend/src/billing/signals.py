from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from billing.models import BillingProfile
from billing.services import BillingProfileToolkit


@receiver(post_save, sender=BillingProfile)
def post_save_billing_profile_receiver(sender, instance: BillingProfile, *args, **kwargs):
    if instance.customer_id is None:
        if settings.STRIPE_API_TURNED_ON:
            BillingProfileToolkit.create_new_customer(billing_profile=instance)

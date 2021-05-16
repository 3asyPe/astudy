from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from billing.services import BillingProfileToolkit
from carts.services import WishlistToolkit


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def post_save_user_create_receiver(sender, instance=None, created=False, **kwargs):
    if created:
        WishlistToolkit.create_new_wishlist(user=instance)
        BillingProfileToolkit.create_new_billing_profile(user=instance)

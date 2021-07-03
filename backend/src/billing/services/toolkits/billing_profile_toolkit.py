from django.conf import settings

from app.integrations.stripe import AppStripe
from billing.models import BillingProfile
from billing.services import BillingProfileCreator


User = settings.AUTH_USER_MODEL


class BillingProfileToolkit:
    @classmethod
    def create_new_billing_profile(cls, user: User) -> BillingProfile:
        return BillingProfileCreator(user=user)()

    @classmethod
    def create_new_customer(cls, billing_profile):
        customer = AppStripe.create_customer(email=billing_profile.user.email)
        billing_profile.customer_id = customer["id"]
        billing_profile.save()
        return billing_profile

    @classmethod
    def get_or_create_billing_profile(cls, user: User) -> BillingProfile:
        qs = BillingProfile.objects.filter(user=user)
        if qs.exists():
            return qs.first()
        return cls.create_new_billing_profile(user=user)

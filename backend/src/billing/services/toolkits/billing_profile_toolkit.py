from django.conf import settings

from billing.models import BillingProfile
from billing.services import BillingProfileCreator


User = settings.AUTH_USER_MODEL


class BillingProfileToolkit:
    @classmethod
    def create_new_billing_profile(cls, user: User) -> BillingProfile:
        return BillingProfileCreator(user=user)()
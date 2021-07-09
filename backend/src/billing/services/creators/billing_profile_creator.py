from typing import Optional

from django.conf import settings

from accounts.utils import AccountErrorMessages
from app.errors import ValidationError
from app.integrations.stripe import AppStripe
from billing.models import BillingProfile
from billing.utils import BillingProfileErrorMessages


User = settings.AUTH_USER_MODEL


class BillingProfileCreator:
    def __init__(
        self, 
        user: User, 
        country: Optional[str] = None, 
        customer_id: Optional[str] = None,
    ):
        self.user = user if user.is_authenticated else None
        self.country = country
        self.customer_id = customer_id

    def __call__(self) -> BillingProfile:
        if self.allowed_to_create(raise_exception=True):
            billing_profile = self.create()
            return billing_profile

    def create(self) -> BillingProfile:
        billing_profile = BillingProfile.objects.create(user=self.user)
        if self.country:
            billing_profile.country = self.country
        if self.customer_id:
            billing_profile.customer_id = self.customer_id
        billing_profile.save()

        return billing_profile

    def allowed_to_create(self, raise_exception=False) -> bool:
        try:
            if self.user is None:
                raise ValidationError(AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value)
            if BillingProfile.objects.filter(user=self.user, active=True).exists():
                raise ValidationError(BillingProfileErrorMessages.BILLING_PROFILE_ALREADY_EXISTS_ERROR.value)
        except ValidationError as exc:
            if raise_exception:
                raise exc
            else:
                return False
        return True

from typing import Optional

from django.conf import settings

from app.errors import ValidationError
from app.integrations.stripe import AppStripe
from billing.models import Card
from orders.models import PaymentMethod
from orders.utils import PaymentMethodErrorMessages


class PaymentMethodCreator:
    def __init__(self, type: str, stripe_id: str, card: Optional[Card]=None):
        self.type = type
        self.stripe_id = stripe_id
        self.card = card

    def __call__(self) -> Optional[PaymentMethod]:
        if self.allowed_to_create():
            obj = self.create()
            if self.type == "CARD":
                obj.card = self.card
                obj.save()            
            return obj
        return None
        
    def create(self) -> PaymentMethod:
        return PaymentMethod.objects.create(
            type=self.type,
            stripe_id=self.stripe_id,
        )

    def allowed_to_create(self) -> bool:
        if not self.type in dict(settings.PAYMENT_METHODS):
            raise ValidationError(PaymentMethodErrorMessages.UNSUPPORTED_PAYMENT_METHOD_TYPE_ERROR.value)

        if not self.stripe:
            raise ValidationError(PaymentMethodErrorMessages.WRONG_STRIPE_ID_ERROR.value)

        return True

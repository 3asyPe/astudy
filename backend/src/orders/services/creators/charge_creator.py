import logging
import stripe.error

from app.errors import ValidationError
from app.integrations.stripe import AppStripe
from app.integrations.stripe.errors import (
    UnknownStripeError, 
    StripeResponseFieldError, 
    NotChargedStripeError,
)
from app.integrations.stripe.utils import StripeErrorMessages
from orders.models import Order, Charge
from orders.utils import ChargeErrorMessages


logger = logging.getLogger(__name__)


class ChargeCreator:
    def __init__(self, order):
        self.order = order
        self.billing_profile = order.billing_profile
        self.payment_method = order.payment_method
        self.amount = order.total

        self.stripe_id = None

    def __call__(self) -> Charge:
        if self.allowed_to_create():
            self.create_stripe_charge()
            return self.create()
        return None

    def create(self):
        return Charge.objects.create(
            order=self.order,
            billing_profile=self.billing_profile,
            payment_method=self.payment_method,
            amount=self.amount,
            stripe_id=self.stripe_id,
        )

    def create_stripe_charge(self):
        try:
            response = dict(AppStripe.create_charge(
                customer_id=self.billing_profile.customer_id,
                token=self.payment_method.stripe_token,
                amount=self.amount,
                metadata={
                    "order_id": self.order.order_id,
                }
            ))

            paid = response["paid"]
            if not paid:
                logger.info(f"Order with id -{self.order.order_id} wasn't charged. Reason - {response['failure_message']}")
                raise NotChargedStripeError(response["failure_message"])
        except stripe.error.InvalidRequestError as exc:
            self._raise_stripe_response_error(exc)

        self._parse_stripe_response(response)

    def allowed_to_create(self) -> bool:
        if self.amount < 1:
            raise ValidationError(ChargeErrorMessages.TOO_SMALL_AMOUNT_ERROR.value)
        
        return True

    def _parse_stripe_response(self, response):
        try:
            self.stripe_id = response["id"]
        except KeyError as exc:
            logger.error(f"StripeResponseFieldError was raised -> {exc}")
            raise StripeResponseFieldError(exc)

    def _raise_stripe_response_error(self, exc):
        message = dict(exc.error)["message"]
        if "No such token" in message:
            raise ValidationError(StripeErrorMessages.WRONG_STRIPE_TOKEN_ERROR.value)

        if "No such customer" in message:
            raise ValidationError(StripeErrorMessages.WRONG_STRIPE_CUSTOMER_ID.value)

        logger.error(f"UnknownStripeError was raised -> {exc}")
        raise UnknownStripeError(exc)

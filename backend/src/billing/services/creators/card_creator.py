import logging
import stripe.error

from typing import Optional

from app.errors import ValidationError
from app.integrations.stripe import AppStripe
from app.integrations.stripe.errors import UnknownStripeError, StripeResponseFieldError
from app.integrations.stripe.utils import StripeErrorMessages
from billing.models import Card
from billing.utils import CardErrorMessages


logger = logging.getLogger(__name__)


class CardCreator:
    def __init__(self, billing_profile, stripe_token, default=False):
        self.billing_profile = billing_profile
        self.customer_id = billing_profile.customer_id
        self.stripe_token = stripe_token

        self.stripe_id = None
        self.brand = None
        self.country = None
        self.postal_code = None
        self.exp_month = None
        self.exp_year = None
        self.last4 = None
        self.cvc_check = "unckecked"

        self.default = default

    def __call__(self) -> Optional[Card]:
        self.create_stripe_card()
        if self.allowed_to_create():
            card = self.create()
            if self.default:
                card.set_as_default()
            return card
        return None

    def create(self):
        return Card.objects.create(
            billing_profile=self.billing_profile,
            stripe_id=self.stripe_id,
            brand=self.brand,
            country=self.country,
            postal_code=self.postal_code,
            exp_month=self.exp_month,
            exp_year=self.exp_year,
            last4=self.last4,
        )

    def create_stripe_card(self):
        try:
            response = dict(AppStripe.create_card(
                customer_id=self.customer_id, 
                token=self.stripe_token
            ))
        except stripe.error.InvalidRequestError as exc:
            self._raise_stripe_response_error(exc)

        self._parse_stripe_response(response)

    def allowed_to_create(self) -> bool:
        if not self.stripe_id.startswith("card_"):
            raise ValidationError(CardErrorMessages.WRONG_CARD_STRIPE_ID_ERROR.value)

        if not self.brand:
            raise ValidationError(CardErrorMessages.WRONG_CARD_BRAND_ERROR.value)

        if not self.last4 or len(self.last4) != 4:
            raise ValidationError(CardErrorMessages.WRONG_CARD_LAST4_ERROR.value)

        if self.cvc_check != "pass":
            logger.warning(f"CVC check of card - {self.last4} showed {self.cvc_check}")

        return True

    def _parse_stripe_response(self, response):
        try:
            self.stripe_id = response["id"]
            self.brand = response["brand"]
            self.last4 = response["last4"]
        except KeyError as exc:
            logger.error(f"StripeResponseFieldError was raised -> {exc}")
            raise StripeResponseFieldError(exc)

        self.postal_code = response.get("address_zip")
        self.exp_month = response.get("exp_month")
        self.exp_year = response.get("exp_year")
        self.country = response.get("country")
        self.cvc_check = response.get("cvc_check")

    def _raise_stripe_response_error(self, exc):
        message = dict(exc.error)["message"]
        if "No such token" in message:
            raise ValidationError(StripeErrorMessages.WRONG_STRIPE_TOKEN_ERROR.value)

        if "No such customer" in message:
            raise ValidationError(StripeErrorMessages.WRONG_STRIPE_CUSTOMER_ID.value)

        logger.error(f"UnknownStripeError was raised -> {exc}")
        raise UnknownStripeError(exc)

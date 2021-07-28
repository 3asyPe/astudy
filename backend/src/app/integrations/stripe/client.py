import stripe
import logging

from django.conf import settings


logger = logging.getLogger(__name__)


if settings.STRIPE_API_TURNED_ON:
    stripe.api_key = settings.STRIPE_API_KEY


class AppStripe:
    customer = stripe.Customer
    token = stripe.Token
    charge = stripe.Charge

    @classmethod
    def create_customer(cls, email):
        return cls.customer.create(email=email)

    @classmethod
    def get_customer(cls, customer_id):
        return cls.customer.retrieve(customer_id)

    @classmethod
    def delete_customer(cls, customer_id):
        return cls.customer.delete(customer_id)

    @classmethod
    def create_card(cls, customer_id, token):
        return cls.customer.create_source(customer_id, source=token)

    @classmethod
    def retrieve_card(cls, customer_id, card_id):
        return cls.customer.retrieve_source(customer_id, card_id)

    @classmethod
    def delete_card(cls, customer_id, card_id):
        return cls.customer.retrieve_source(customer_id, card_id)

    @classmethod
    def retrieve_token(cls, token):
        return cls.token.retrieve(token)

    @classmethod
    def create_charge(cls, customer_id, token, amount, metadata={}):
        return cls.charge.create(
            amount=int(amount*100), # Stripe interpret 1111$ as 11.11$
            currency="usd",
            customer=customer_id,
            source=token,
            metadata=metadata,
        )

    @classmethod
    def validate_token(cls, token) -> bool:
        try:
            cls.retrieve_token(token=token)
            return True
        except stripe.error.InvalidRequestError:
            return False

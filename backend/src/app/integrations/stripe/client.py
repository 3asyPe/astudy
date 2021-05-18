import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY


class AppStripe:
    customer = stripe.Customer

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
        return cls.customer.retrive_source(customer_id, card_id)

    @classmethod
    def delete_card(cls, customer_id, card_id):
        return cls.customer.retrieve_source(customer_id, card_id)

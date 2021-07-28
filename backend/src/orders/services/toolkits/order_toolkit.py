import logging

from typing import Optional

from django.db import transaction

from app.errors import UnknownError
from billing.models import BillingProfile, Card
from billing.services import CardCreator
from carts.models import Cart
from orders.models import Order, PaymentMethod, Charge
from orders.services import OrderCreator, PaymentMethodCreator, ChargeCreator


logger = logging.getLogger(__name__)


class OrderToolkit:
    @classmethod
    @transaction.atomic
    def complete_order(
        cls,
        billing_profile: BillingProfile, 
        cart: Cart,
        card_last4: Optional[str] = None,
        stripe_token: Optional[str] = None, 
        save_card: bool = False,
    ) -> Order:
        order = cls.place_an_order(
            billing_profile=billing_profile,
            cart=cart,
            stripe_token=stripe_token,
            card_last4=card_last4,
            save_card=save_card,
        )
        if order is None:
            logger.error(f"An UnknownError was raised when creating order {order.order_id}")
            raise UnknownError() 
        logger.info(f'Order with id - {order.order_id} has been created')

        charge = cls.charge_for_order(order)
        if charge is None:
            logger.error(f"An UnknownError was raised when creating charge for order {order.order_id}")
            raise UnknownError()
        order.set_paid(paid=True)
        logger.info(f"Charge for order with id - {order.order_id} has been created")

        order = cls.ship_order(order)
        order.set_shipped(shipped=True)
        logger.info(f"Order with id - {order.order_id} has been shipped")

        order = cls.close_order(order)
        logger.info(f"Order with id - {order.order_id} has been closed")

        return order

    @classmethod
    def place_an_order(
        cls, 
        billing_profile: BillingProfile, 
        cart: Cart,
        card_last4: Optional[str] = None,
        stripe_token: Optional[str] = None, 
        save_card: bool = False,
    ) -> Order:
        card = None
        if card_last4:
            card = Card.objects.get(billing_profile=billing_profile, last4=card_last4)
            stripe_token = card.stripe_id
        elif save_card:
            card = CardCreator(
                billing_profile=billing_profile, 
                stripe_token=stripe_token,
                default=True,
            )()
        
        payment_method = PaymentMethodCreator(
            type="CARD",
            stripe_token=stripe_token,
            card=card
        )()

        order = OrderCreator(
            billing_profile=billing_profile,
            cart=cart,
            payment_method=payment_method,
        )()

        return order

    @classmethod
    def charge_for_order(cls, order) -> Charge:
        return ChargeCreator(order)()

    @classmethod
    def ship_order(cls, order) -> Order:
        return order
    
    @classmethod
    def close_order(cls, order) -> Order:
        order.cart.deactivate()
        return order

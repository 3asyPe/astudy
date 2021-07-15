from billing.models import BillingProfile, Card
from billing.services import CardCreator
from carts.models import Cart
from orders.models import Order, PaymentMethod
from orders.services import OrderCreator, PaymentMethodCreator


class OrderToolkit:
    @classmethod
    def place_an_order(
        cls, 
        billing_profile: BillingProfile, 
        cart: Cart,
        stripe_token: str, 
        save_card: bool = False,
    ) -> Order:
        card = None
        if save_card:
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
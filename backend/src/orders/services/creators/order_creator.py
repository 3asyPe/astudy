from app.errors import ValidationError
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order, PaymentMethod
from orders.utils import OrderErorrMessages


class OrderCreator:
    def __init__(self, billing_profile: BillingProfile, cart: Cart, payment_method: PaymentMethod):
        self.billing_profile = billing_profile
        self.cart = cart
        self.total = cart.total
        self.payment_method = payment_method

    def __call__(self) -> Order:
        if self.allowed_to_create():
            return self.create()
        return None

    def create(self) -> Order:
        return Order.objects.create(
            billing_profile=self.billing_profile,
            cart=self.cart, 
            total=self.total,
            payment_method=self.payment_method,           
        )

    def allowed_to_create(self) -> bool:
        if self.cart.courses.count() == 0:
            raise ValidationError(OrderErorrMessages.EMPTY_CART_ERROR.value)
        
        return True
            
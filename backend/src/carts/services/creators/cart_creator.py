import logging

from typing import Optional

from django.conf import settings

from app.errors import ValidationError
from carts.models import Cart
from carts.utils import CartErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class CartCreator:
    def __init__(self, user: Optional[User]):
        self.user = user if user.is_authenticated else None

    def __call__(self) -> Optional[Cart]:
        if self._allowed_to_create():
            cart = self.create()
            return cart
        raise ValidationError(CartErrorMessages.CART_ALREADY_EXISTS_ERROR.value)


    def create(self) -> Cart:
        return Cart.objects.create(user=self.user)


    def _allowed_to_create(self) -> bool:
        if self.user is not None:
            qs = Cart.objects.filter(user=self.user, active=True)
            if qs.exists():
                logger.error("Active cart for user - {user} already exists and won't be created one more time")
                return False
        return True

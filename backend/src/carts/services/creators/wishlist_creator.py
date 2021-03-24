import logging

from django.conf import settings

from accounts.utils import AccountErrorMessages
from carts.models import Wishlist
from carts.utils import CartErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class WishlistCreator:
    def __init__(self, user: User):
        self.user = user

    def __call__(self) -> Wishlist:
        if self._allowed_to_create():
            wishlist = self.create()
            return wishlist
        raise PermissionError(AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value)

    def create(self) -> Wishlist:
        return Wishlist.objects.create(user=self.user)

    def _allowed_to_create(self) -> bool:
        if not self.user.is_authenticated:
            logger.error("There was an attempt to create a wishlist with a user that wasn't authenticated")
            return False
        return True

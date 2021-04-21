import logging

from django.conf import settings

from accounts.utils import AccountErrorMessages
from app.errors import ValidationError
from carts.models import Wishlist
from carts.utils import WishlistErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class WishlistCreator:
    def __init__(self, user: User):
        self.user = user

    def __call__(self) -> Wishlist:
        if self.allowed_to_create():
            wishlist = self._create()
            return wishlist

    def _create(self) -> Wishlist:
        return Wishlist.objects.create(user=self.user)

    def allowed_to_create(self) -> bool:
        if not self.user.is_authenticated:
            logger.error("There was an attempt to create a wishlist with a user that wasn't authenticated")
            raise PermissionError(AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value)

        qs = Wishlist.objects.filter(user=self.user)
        if qs.exists():
            raise ValidationError(WishlistErrorMessages.WISHLIST_ALREADY_EXISTS_ERROR.value)
        return True

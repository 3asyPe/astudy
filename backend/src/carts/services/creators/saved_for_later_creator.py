import logging

from typing import Optional

from django.conf import settings

from app.errors import ValidationError
from carts.models import SavedForLater
from carts.utils import SavedForLaterErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class SavedForLaterCreator:
    def __init__(self, user: Optional[User]=None):
        self.user = user if user is not None and user.is_authenticated else None

    def __call__(self) -> Optional[SavedForLater]:
        if self._allowed_to_create():
            saved_for_later = self.create()
            return saved_for_later
        raise ValidationError(SavedForLaterErrorMessages.SAVED_FOR_LATER_LIST_ALREADY_EXISTS_ERROR.value)
        
    def create(self) -> SavedForLater:
        return SavedForLater.objects.create(user=self.user)
    
    def _allowed_to_create(self) -> bool:
        if self.user is not None:
            qs = SavedForLater.objects.filter(user=self.user)
            if qs.exists():
                logger.error(f"Saved for later list for user - {self.user} already exists won't be created one more time")
                return False
        return True

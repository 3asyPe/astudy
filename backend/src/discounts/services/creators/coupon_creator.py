import datetime
import logging

from typing import List, Optional

from django.conf import settings
from django.utils import timezone

from app.errors import ValidationError
from courses.models import Course
from discounts.models import Coupon
from discounts.utils import DiscountErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class CouponCreator:
    def __init__(
        self, 
        creator: User, 
        code: str,
        applicable_to: List[Course],
        discount: int,
        expires: Optional[datetime.datetime] = None,
    ):
        self.creator = creator if creator.is_authenticated else None
        self.code = code if not code == '' else None
        self.applicable_to = applicable_to
        self.discount = discount
        self.expires = expires if timezone.is_aware(expires) else timezone.make_aware(expires)

    def __call__(self) -> Coupon:
        if self._allowed_to_create():
            return self.create()
        raise ValidationError(DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value)


    def create(self) -> Coupon:
        coupon = Coupon.objects.create(
            creator=self.creator,
            code=self.code,
            discount=self.discount,
            expires=self.expires,
        )
        coupon.applicable_to.set(self.applicable_to)
        return coupon

    def _allowed_to_create(self) -> bool:
        if self.creator is None:
            logger.error(f"Not authorized user tried to create a coupon with code - {self.code}")
            return False

        if self.code is None or Coupon.objects.filter(code=self.code).exists():
            return False

        if timezone.now() > self.expires:
            logger.error(f"There was an attempt to create a coupon with code - {self.code} with expired date")
            return False

        if not 0 < self.discount < 100:
            logger.error(f"There was an attempt to create a coupon with code - {self.code} with invalid discount")
            return False

        return True
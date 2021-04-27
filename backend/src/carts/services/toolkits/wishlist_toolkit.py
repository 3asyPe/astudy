import logging

from typing import Optional

from django.conf import settings

from app.errors import ValidationError
from accounts.utils import AccountErrorMessages
from carts.models import Wishlist
from carts.services import WishlistCreator
from carts.utils import WishlistErrorMessages
from courses.services import CourseSelector


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class WishlistToolkit:
    @classmethod
    def load_wishlist(cls, user: User) -> Wishlist:
        if not user.is_authenticated:
            raise PermissionError(AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value)
        wishlist = cls._get_wishlist_by_user(user=user)
        if wishlist is None:
            wishlist = cls._create_wishlist(user=user)
        return wishlist

    @classmethod
    def create_new_wishlist(cls, user: User) -> Wishlist:
        if not user.is_authenticated:
            raise PermissionError(AccountErrorMessages.USER_IS_NOT_AUTHENTICATED_ERROR.value)
        if cls._get_wishlist_by_user(user=user) is not None:
            raise ValidationError(WishlistErrorMessages.WISHLIST_ALREADY_EXISTS_ERROR.value)
        return cls._create_wishlist(user=user)

    @classmethod
    def add_course_to_wishlist(cls, wishlist: Wishlist, course_slug: str) -> Wishlist:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course not in wishlist.courses.all():
            wishlist.courses.add(course)
        return wishlist
        
    @classmethod
    def remove_course_from_wishlist(cls, wishlist: Wishlist, course_slug: str) -> Wishlist:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course in wishlist.courses.all():
            wishlist.courses.remove(course)
        return wishlist

    @classmethod
    def check_on_course_in_wishlist(cls, wishlist: Wishlist, course_slug) -> bool:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        return course in wishlist.courses.all()

    @classmethod
    def _get_wishlist_by_user(cls, user: User) -> Optional[Wishlist]:
        qs = Wishlist.objects.filter(user=user)
        if not qs.exists():
            return None
        return qs.first()

    @classmethod
    def _create_wishlist(cls, user: User) -> Optional[Wishlist]:
        return WishlistCreator(user=user)()

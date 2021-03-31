import logging

from typing import Union

from carts.models import Cart, Wishlist, SavedForLater
from courses.models import Course
from courses.services import CourseSelector


logger = logging.getLogger(__name__)


class CartListsToolkit:
    @classmethod
    def delete_duplicates_excluding_instance(
        cls, 
        course_slug: str, 
        instance: Union[Cart, Wishlist, SavedForLater], 
        *args, 
        **kwargs
    ):
        logger.debug(instance)
        logger.debug(kwargs)
        course = CourseSelector.get_course_by_slug(slug=course_slug)

        cart = kwargs.get("cart")
        if cart and cart is not instance and course in cart.courses.all():
            cart.courses.remove(course)

        wishlist = kwargs.get("wishlist")
        if wishlist and wishlist is not instance and course in wishlist.courses.all():
            wishlist.courses.remove(course)
        
        saved_for_later = kwargs.get("saved_for_later")
        if saved_for_later and saved_for_later is not instance and course in saved_for_later.courses.all():
            saved_for_later.courses.remove(course)

    @classmethod
    def get_cart_lists_ids_from_request(cls, request) -> dict:
        data = request.GET or request.POST
        cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
        saved_for_later_id = int(data.get("saved_for_later_id")) if data.get("saved_for_later_id") is not None else None
        return {
            "cart_id": cart_id,
            "saved_for_later_id": saved_for_later_id,
        }
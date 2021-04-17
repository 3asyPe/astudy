import logging

from typing import Optional

from django.conf import settings

from carts.models import Cart
from carts.services import CartCreator
from courses.services import CourseSelector
from discounts.services import DiscountSelector


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class CartToolkit:
    @classmethod
    def load_cart(cls, user: Optional[User] = None, cart_id: Optional[int] = None) -> Cart:
        cart = None
        if user is None or not user.is_authenticated:
            cart_by_user_qs = Cart.objects.none()
        else:
            cart_by_user_qs = Cart.objects.filter(user=user, active=True)
        
        cart_by_id_qs = Cart.objects.filter(id=cart_id, active=True)
        if cart_by_id_qs.exists() and cart_by_user_qs.exists():
            cart_by_id = cart_by_id_qs.last()
            cart_by_user = cart_by_user_qs.last()
            cart = cls._choose_cart_by_user_or_by_id(cart_by_id, cart_by_user)
        elif cart_by_user_qs.exists():
            cart = cart_by_user_qs.last()
        elif cart_by_id_qs.exists():
            cart_by_id = cart_by_id_qs.last()
            if user is not None and user.is_authenticated:
                if cart_by_id.user is None:
                    cart_by_id.user = user
                    cart_by_id.save()
                    cart = cart_by_id
                elif cart_by_id.user != user:
                    cart = cls._create_new_cart(user=user)
                else:
                    cart = cart_by_id
            else:
                cart = cart_by_id
        else:
            cart = cls._create_new_cart(user=user)
            
        cart.update_totals()
        return cart

    @classmethod
    def add_course_to_cart(cls, cart: Cart, course_slug: str) -> Cart:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course not in cart.courses.all():
            cart.courses.add(course)
        return cart

    @classmethod
    def remove_course_from_cart(cls, cart: Cart, course_slug: str) -> Cart:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course in cart.courses.all():
            cart.courses.remove(course)
        return cart

    @classmethod
    def check_on_course_in_cart(cls, cart: Cart, course_slug: str) -> bool:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        return course in cart.courses.all()

    @classmethod
    def update_cart_totals(cls, cart: Cart) -> Cart:
        courses = CourseSelector.get_courses_by_cart(cart=cart)
        subtotal = 0
        total = 0
        for course in courses:
            subtotal += course.price
            discount = DiscountSelector.get_discount_for_course_or_nothing(course=course, cart=cart)
            if discount is None:
                total += course.price
            else:
                total += discount.new_price
        cart.subtotal = subtotal
        cart.total = total
        cart.save()
        return cart

    @classmethod
    def _create_new_cart(cls, user=None) -> Cart:
        return CartCreator(user=user)()

    @classmethod
    def _choose_cart_by_user_or_by_id(cls, cart_by_id: Cart, cart_by_user: Cart) -> Cart:
        if cart_by_id != cart_by_user:
            if cart_by_id.user is not None and cart_by_id.user != cart_by_user.user:
                return cart_by_user
            if cart_by_user.get_courses_count != 0:
                cart_by_id.delete()
                return cart_by_user
            else:
                if cart_by_id.user is None:
                    cart_by_id.user = cart_by_user.user
                    cart_by_id.save()
                cart_by_user.delete()
                return cart_by_id
        return cart_by_id

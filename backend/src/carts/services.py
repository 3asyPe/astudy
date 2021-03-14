import logging

from app.errors import ValidationError
from courses.models import Course
from courses.selectors import get_course_by_slug
from django.conf import settings

from .models import Cart
from .utils import CartErrorMessages


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


def update_cart_totals(cart: Cart) -> Cart:
    courses = cart.courses.all()
    total = 0
    for course in courses:
        total += course.price
    if cart.subtotal != total:
        cart.subtotal = total
        cart.save()
    return cart


def load_cart(user: User, cart_id=None) -> Cart:
    cart = None
    if not user.is_authenticated:
        cart_by_user_qs = Cart.objects.none()
    else:
        cart_by_user_qs = Cart.objects.filter(user=user, active=True)
    
    cart_by_id_qs = Cart.objects.filter(id=cart_id, active=True)
    if cart_by_id_qs.exists() and cart_by_user_qs.exists():
        cart_by_id = cart_by_id_qs.last()
        cart_by_user = cart_by_user_qs.last()
        cart = _choose_cart_by_user_or_by_id(cart_by_id, cart_by_user)
    elif cart_by_user_qs.exists():
        cart = cart_by_user_qs.last()
    elif cart_by_id_qs.exists():
        cart_by_id = cart_by_id_qs.last()
        if user.is_authenticated and cart_by_id.user is None:
            cart_by_id.user = user
            cart_by_id.save()
        cart = cart_by_id
    else:
        cart = create_new_cart(user=user)
    return cart


def add_course_to_cart(cart: Cart, course_slug: str) -> Cart:
    course = get_course_by_slug(slug=course_slug)
    if course not in cart.courses.all():
        cart.courses.add(course)
    return cart
    

def remove_course_from_cart(cart: Cart, course_slug: str) -> Cart:
    course = get_course_by_slug(slug=course_slug)
    if course in cart.courses.all():
        cart.courses.remove(course)
    return cart

def create_new_cart(user=None) -> Cart:
    if user is not None:
        if user.is_authenticated:
            qs = Cart.objects.filter(user=user, active=True)
            if qs.exists():
                logger.error("Active cart for user - {user} already exists and won't be created one more time")
                raise ValidationError(CartErrorMessages.CART_ALREADY_EXISTS_ERROR.value)
        else:
            user = None
    return Cart.objects.create(user=user)


def _choose_cart_by_user_or_by_id(cart_by_id: Cart, cart_by_user: Cart) -> Cart:
    if cart_by_id != cart_by_user:
        if cart_by_id.courses.all().count() == 0:
            cart_by_id.delete()
            return cart_by_user
        else:
            cart_by_user.delete()
            return cart_by_id
    return cart_by_id

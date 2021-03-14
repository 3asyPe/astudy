import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CartSerializer
from .services import (
    load_cart, 
    add_course_to_cart,
    remove_course_from_cart,
)
from .utils import CartErrorMessages


logger = logging.getLogger(__name__)


@api_view(["GET"])
def load_cart_api(request, *args, **kwargs):
    data = request.GET
    cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    serializer = CartSerializer(instance=cart)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def add_course_to_cart_api(request, *args, **kwargs):
    try:
        data = request.POST
        cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
        course_slug = data["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    cart = add_course_to_cart(cart=cart, course_slug=course_slug)
    return Response({}, status=200)


@api_view(["POST"])
def remove_course_from_cart_api(request, *args, **kwargs):
    try:
        data = request.POST
        cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
        course_slug = data["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    cart = remove_course_from_cart(cart=cart, course_slug=course_slug)
    return Response({}, status=200)


@api_view(["GET"])
def get_cart_courses_count_api(request, *args, **kwargs):
    data = request.GET
    cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    return Response({"cart_courses_count": cart.get_courses_count()}, status=200)

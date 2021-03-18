import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carts.serializers import CartSerializer, WishlistSerializer
from carts.services import CartToolkit, WishlistToolkit
from carts.utils import CartErrorMessages


logger = logging.getLogger(__name__)


@api_view(["GET"])
def load_cart_api(request, *args, **kwargs):
    data = request.GET
    cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
    user = request.user
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    serializer = CartSerializer(instance=cart)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def load_wishlist_api(request, *args, **kwargs):
    user = request.user
    wishlist = WishlistToolkit.load_wishlist(user=user)
    serializer = WishlistSerializer(instance=wishlist)
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
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    cart = CartToolkit.add_course_to_cart(cart=cart, course_slug=course_slug)
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
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    cart = CartToolkit.remove_course_from_cart(cart=cart, course_slug=course_slug)
    return Response({}, status=200)


@api_view(["GET"])
def get_cart_courses_count_api(request, *args, **kwargs):
    data = request.GET
    cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
    user = request.user
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    return Response({
        "cart_courses_count": cart.get_courses_count(), 
        "cart_id": cart.id,
    }, status=200)


@api_view(["GET"])
def check_on_course_already_in_cart(request, *args, **kwargs):
    try:
        data = request.GET
        cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
        course_slug = data["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    course_already_in_cart = CartToolkit.check_on_course_in_cart(cart=cart, course_slug=course_slug)
    return Response({"course_already_in_cart": course_already_in_cart}, status=200)

import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ValidationError
from carts.services import (
    CartToolkit,
    CartListsToolkit,
    CartListsSelector,
)
from carts.serializers import CartDiscountsInfoSerializer
from discounts.services import CouponToolkit
from discounts.utils import DiscountErrorMessages


logger = logging.getLogger(__name__)


@api_view(["POST"])
def apply_coupon_api(request, *args, **kwargs):
    try:
        coupon_code = request.POST["coupon_code"]
    except KeyError:
        logger.error("Request object doesn't have a coupon code")
        return Response({"error": DiscountErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    cart = cart_lists["cart"]
    wishlist = cart_lists["wishlist"]
    saved_for_later=cart_lists["saved_for_later"]

    try:
        CouponToolkit.apply_coupon(code=coupon_code, cart=cart)
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    context={
        "saved_for_later": saved_for_later,
        "wishlist": wishlist,
    }
    serializer = CartDiscountsInfoSerializer(instance=cart, context=context)
    
    return Response(serializer.data, status=200)



@api_view(["POST"])
def remove_applied_coupon_api(request, *args, **kwargs):
    try:
        coupon_code = request.POST["coupon_code"]
    except KeyError:
        logger.error("Request object doesn't have a coupon code")
        return Response({"error": DiscountErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    cart = cart_lists["cart"]
    wishlist = cart_lists["wishlist"]
    saved_for_later=cart_lists["saved_for_later"]

    CouponToolkit.remove_applied_coupon(code=coupon_code, cart=cart)

    context={
        "saved_for_later": saved_for_later,
        "wishlist": wishlist,
    }
    serializer = CartDiscountsInfoSerializer(instance=cart, context=context)

    return Response(serializer.data, status=200)
import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ValidationError
from carts.services import (
    CartToolkit,
    CartListsToolkit,
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

    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart = CartToolkit.load_cart(user=user, cart_id=ids["cart_id"])

    try:
        CouponToolkit.apply_coupon(code=coupon_code, cart=cart)
    except ValidationError as exc:
        logger.debug(exc)
        return Response({"error": str(exc)}, status=400)

    serializer = CartDiscountsInfoSerializer(instance=cart)
    
    return Response(serializer.data, status=200)



@api_view(["POST"])
def remove_applied_coupon_api(request, *args, **kwargs):
    try:
        coupon_code = request.POST["coupon_code"]
    except KeyError:
        logger.error("Request object doesn't have a coupon code")
        return Response({"error": DiscountErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart = CartToolkit.load_cart(user=user, cart_id=ids["cart_id"])

    CouponToolkit.remove_applied_coupon(code=coupon_code, cart=cart)

    serializer = CartDiscountsInfoSerializer(instance=cart)

    return Response(serializer.data, status=200)
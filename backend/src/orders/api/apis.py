import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.errors import ValidationError
from billing.services import BillingProfileToolkit
from carts.services import CartToolkit
from orders.services import OrderToolkit


logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_order_api(request, *args, **kwargs):
    data = request.POST
    billing_profile = BillingProfileToolkit.get_or_create_billing_profile(user=request.user)
    cart = CartToolkit.load_cart(user=request.user)
    try:
        stripe_token = data.get("card_token")
        country = data["country"]
        payment_method = data["payment_method"]

        remember_card = False
        if payment_method == "newPaymentCard":
            remember_card = data["remember_card"] == "true"

        card_last4 = None
        if len(payment_method) == 4:
            card_last4 = payment_method
    except KeyError:
        return Response({"error": "Request object doesn't have required fields"}, 400)

    billing_profile.country = country
    billing_profile.save()

    try:
        order = OrderToolkit.place_an_order(
            billing_profile=billing_profile,
            cart=cart,
            stripe_token=stripe_token,
            card_last4=card_last4,
            save_card=remember_card,
        )
    except ValidationError as exc:
        return Response({"error": str(exc.value)}, status=400)

    logger.info(f'Order with id - {order.id} has been created')
    
    return Response({"order_id": order.order_id}, 200)

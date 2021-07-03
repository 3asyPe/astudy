from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from billing.services import BillingProfileToolkit
from billing.api.serializers import BillingProfileSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_billing_profile_api(request):
    billing_profile = BillingProfileToolkit.get_or_create_billing_profile(user=request.user)
    serializer = BillingProfileSerializer(instance=billing_profile)
    return Response(serializer.data, status=200)

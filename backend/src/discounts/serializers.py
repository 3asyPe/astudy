from rest_framework import serializers

from discounts.models import AppliedCoupon


class AppliedCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedCoupon
        fields = ["code"]

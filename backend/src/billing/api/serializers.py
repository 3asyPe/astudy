from rest_framework import serializers

from billing.models import BillingProfile, Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'brand',
            'last4',
            'default',
        ]

        
class BillingProfileSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = BillingProfile
        fields = [
            'country',
            'cards',
        ]

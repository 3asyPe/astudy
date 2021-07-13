from typing import Optional

from billing.models import BillingProfile, Card


class CardCreator:
    def __init__(self, billing_profile: BillingProfile, stripe_id: str):
        self.billing_profile = billing_profile
        self.stripe_id = stripe_id

    def __call__(self) -> Optional[Card]:
        if self.allowed_to_create():
            return self.create()
        return None

    def create(self) -> Card:
        return None

    def allowed_to_create(self) -> bool:
        return False
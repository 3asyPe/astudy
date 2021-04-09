from django.contrib import admin

from discounts.models import AppliedCoupon


@admin.register(AppliedCoupon)
class AppliedCouponAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "user_email",
        "cart_id",
        "active"
    ]

    list_display_links = [
        "id",
        "code",
        "user_email",
        "cart_id",
    ]

    list_filter = [
        "active",
    ]

    def code(self, obj):
        return obj.code

    def user_email(self, obj):
        if obj.cart.user:
            return obj.cart.user.email
        return "Not authorized"

    def cart_id(self, obj):
        return obj.cart.id

from django.contrib import admin

from discounts.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "discount",
        "expires",
        "active"
    ]

    list_display_links = [
        "id",
        "code",
        "discount",
        "expires",
    ]

    list_filter = [
        "active"
    ]
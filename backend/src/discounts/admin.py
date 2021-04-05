from django.contrib import admin

from discounts.models import AppliedCoupon, Coupon


admin.site.register(Coupon)
admin.site.register(AppliedCoupon)
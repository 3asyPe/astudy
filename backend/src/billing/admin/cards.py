from django.contrib import admin

from billing.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'brand',
        'last4',
        'active',
    ]

    list_display_links = [
        'id',
        'user',
        'brand',
        'last4',
        'active',
    ]

    fields = [
        'billing_profile',
        'stripe_id',
        'brand',
        'country',
        'exp_month',
        'exp_year',
        'last4',
        'default',
        'active',
    ]

    readonly_fields = [
        'timestamp',
    ]

    list_filters = [
        'active',
        'brand',
        'country',
        'default',
    ]

    def user(self, obj):
        return str(obj.billing_profile.user)
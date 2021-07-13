from django.contrib import admin

from billing.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'brand',
        'last4',
    ]

    list_display_links = [
        'id',
        'user',
        'brand',
        'last4',
    ]

    fields = [
        'brand',
        'country',
        'exp_month',
        'exp_year',
        'last4',
    ]

    readonly_fields = [
        'timestamp',
    ]

    list_filters = [
        'brand',
        'country',
    ]

    def user(self, obj):
        return str(obj.billing_profile.user)
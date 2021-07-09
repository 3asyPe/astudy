from django.contrib import admin

from billing.models import BillingProfile


@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'country',
        'active',
    ]

    list_display_links = [
        'id',
        'user',
        'country',
        'active'
    ]

    fields = [
        'user',
        'country',
        'customer_id',
        'active',
    ]

    readonly_fields = [
        'updated',
        'timestamp',
    ]

    list_filter = [
        'active',
        'country',
    ]
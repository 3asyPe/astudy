from django.contrib import admin

from app.admin import UserFilter
from billing.models import BillingProfile


@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'country',
        'postal_code',
        'active',
    ]

    list_display_links = [
        'id',
        'user',
        'country',
        'postal_code',
        'active'
    ]

    fields = [
        'user',
        'country',
        'postal_code',
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
        UserFilter
    ]
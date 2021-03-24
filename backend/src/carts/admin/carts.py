from django.contrib import admin

from app.admin import UserFilter
from carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'total', 
        'active',
    ]

    list_display_links = [
        'id',
        'user',
        'total',
        'active'
    ]

    fields = [
        "user",
        "courses",
        "subtotal",
        "total",
        "active",
    ]

    readonly_fields = [
        "subtotal",
        "total",
    ]

    list_filter = [
        'active',
        UserFilter
    ]

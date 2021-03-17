from django.contrib import admin

from .models import Cart


class UserFilter(admin.SimpleListFilter):
    title = "User"
    parameter_name = "user"

    def lookups(self, request, model_admin):
        return (
            ("has_user", "Has a user"),
            ("no_user", "Doesn't have a user"),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == "has_user":
            return queryset.exclude(user=None)
        if self.value().lower() == "no_user":
            return queryset.filter(user=None)


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

    list_filter = [
        'active',
        UserFilter
    ]